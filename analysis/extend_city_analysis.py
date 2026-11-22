"""Extend the city-level restaurant analysis with socioeconomic context.

Inputs are the previously generated 2024 ACS / OSM city dataset and the
original 2024 TIGER/Line place files.  Additional 2024 ACS 5-year variables
are read from the Census Bureau table-based summary files so the release is
consistent for every city, including places below the ACS 1-year threshold.
"""

from __future__ import annotations

import csv
import json
import math
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats


ROOT = Path("/workspace/scratch/cabc89d17390")
PROCESSED = ROOT / "work/city_scale/processed"
RAW = ROOT / "work/city_scale/raw"
OUT = ROOT / "work/city_scale/extended"
OUT.mkdir(parents=True, exist_ok=True)

ACS_BASE = (
    "https://www2.census.gov/programs-surveys/acs/summary_file/2024/"
    "table-based-SF/data/5YRData"
)


def read_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def valid_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    # ACS negative sentinels represent unavailable or suppressed estimates.
    return number if math.isfinite(number) and number >= 0 else None


def fetch_table(table_id: str, wanted_geoids: set[str]):
    url = f"{ACS_BASE}/acsdt5y2024-{table_id.lower()}.dat"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Tiger-Xu-restaurant-research/1.1 (educational research)"},
    )
    rows = {}
    with urllib.request.urlopen(request, timeout=180) as response:
        header = response.readline().decode("utf-8").rstrip("\r\n").split("|")
        for raw_line in response:
            line = raw_line.decode("utf-8").rstrip("\r\n")
            if not line:
                continue
            values = line.split("|")
            file_geoid = values[0]
            # Table-based summary files use a seven-character summary-level
            # prefix (1600000US), while the working dataset uses 16000US.
            geoid = file_geoid.replace("1600000US", "16000US", 1)
            if geoid in wanted_geoids:
                rows[geoid] = dict(zip(header, values))
                if len(rows) == len(wanted_geoids):
                    break
    return url, rows


def pearson_summary(rows, x_name, y_name):
    pairs = [
        (valid_number(row.get(x_name)), valid_number(row.get(y_name)))
        for row in rows
    ]
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    x = np.asarray([p[0] for p in pairs], dtype=float)
    y = np.asarray([p[1] for p in pairs], dtype=float)
    pearson = stats.pearsonr(x, y)
    spearman = stats.spearmanr(x, y)
    regression = stats.linregress(x, y)
    return {
        "x": x_name,
        "y": y_name,
        "n": int(len(x)),
        "pearson_r": float(pearson.statistic),
        "pearson_p": float(pearson.pvalue),
        "spearman_rho": float(spearman.statistic),
        "spearman_p": float(spearman.pvalue),
        "slope": float(regression.slope),
        "intercept": float(regression.intercept),
        "r_squared": float(pearson.statistic**2),
    }


def ols_hc3(rows, outcome, predictors):
    complete = []
    for row in rows:
        y = valid_number(row.get(outcome))
        xs = [valid_number(row.get(p)) for p in predictors]
        if y is not None and all(v is not None for v in xs):
            complete.append((row["label"], y, xs))
    labels = [r[0] for r in complete]
    y = np.asarray([r[1] for r in complete], dtype=float)
    raw_x = np.asarray([r[2] for r in complete], dtype=float)
    means = raw_x.mean(axis=0)
    sds = raw_x.std(axis=0, ddof=1)
    z_x = (raw_x - means) / sds
    y_mean = y.mean()
    y_sd = y.std(ddof=1)
    z_y = (y - y_mean) / y_sd
    x = np.column_stack([np.ones(len(y)), z_x])
    xtx_inv = np.linalg.inv(x.T @ x)
    beta = xtx_inv @ x.T @ z_y
    residuals = z_y - x @ beta
    leverage = np.sum((x @ xtx_inv) * x, axis=1)
    scaled = residuals / np.maximum(1 - leverage, 1e-10)
    meat = np.zeros((x.shape[1], x.shape[1]))
    for xi, ei in zip(x, scaled):
        meat += (ei**2) * np.outer(xi, xi)
    covariance = xtx_inv @ meat @ xtx_inv
    se = np.sqrt(np.diag(covariance))
    df = len(y) - x.shape[1]
    t_values = beta / se
    p_values = 2 * stats.t.sf(np.abs(t_values), df=df)
    ss_res = float(np.sum(residuals**2))
    ss_tot = float(np.sum((z_y - z_y.mean()) ** 2))
    r_squared = 1 - ss_res / ss_tot

    coefficients = []
    names = ["Intercept", *predictors]
    for name, b, s, t, p in zip(names, beta, se, t_values, p_values):
        coefficients.append(
            {
                "term": name,
                "standardized_beta": float(b),
                "hc3_se": float(s),
                "t": float(t),
                "p": float(p),
            }
        )

    # Variance inflation factors for the standardized predictors.
    vifs = {}
    for j, name in enumerate(predictors):
        target = z_x[:, j]
        others = np.delete(z_x, j, axis=1)
        aux = np.column_stack([np.ones(len(y)), others])
        aux_beta = np.linalg.lstsq(aux, target, rcond=None)[0]
        aux_resid = target - aux @ aux_beta
        aux_r2 = 1 - np.sum(aux_resid**2) / np.sum((target - target.mean()) ** 2)
        vifs[name] = float(1 / (1 - aux_r2)) if aux_r2 < 1 else None

    return {
        "outcome": outcome,
        "predictors": predictors,
        "n": int(len(y)),
        "r_squared": float(r_squared),
        "adjusted_r_squared": float(1 - (1 - r_squared) * (len(y) - 1) / df),
        "coefficients": coefficients,
        "vif": vifs,
        "standardization": {
            "outcome_mean": float(y_mean),
            "outcome_sd": float(y_sd),
            "predictor_means": dict(zip(predictors, means.tolist())),
            "predictor_sds": dict(zip(predictors, sds.tolist())),
        },
        "labels": labels,
        "note": "Exploratory OLS with HC3 robust standard errors; standardized coefficients; observational and non-causal.",
    }


payload = read_json(PROCESSED / "city_summary.json")
cities = [row for row in payload["cities"] if row.get("query_status") == "Complete"]
wanted_geoids = {row["geoid"] for row in cities}

income_url, income_rows = fetch_table("B19013", wanted_geoids)
birth_url, birth_rows = fetch_table("B05002", wanted_geoids)

land_area = {}
for state_folder in ("ca", "or", "wa"):
    places = read_json(RAW / state_folder / "places.geojson")
    for feature in places["features"]:
        p = feature["properties"]
        geoid = f"16000US{p['GEOID']}"
        if geoid in wanted_geoids:
            land_area[geoid] = valid_number(p.get("ALAND"))

restaurant_geojson = read_json(PROCESSED / "asian_restaurants.geojson")
features_by_city = defaultdict(list)
global_ids = []
for feature in restaurant_geojson["features"]:
    props = feature["properties"]
    features_by_city[props["city_geoid"]].append(props)
    global_ids.append((props.get("osm_type"), props.get("osm_id")))

audit_rows = []
for city in cities:
    geoid = city["geoid"]
    income = income_rows.get(geoid, {})
    birth = birth_rows.get(geoid, {})
    median_income = valid_number(income.get("B19013_E001"))
    foreign_born = valid_number(birth.get("B05002_E013"))
    area_m2 = land_area.get(geoid)
    area_sq_mi = area_m2 / 2_589_988.110336 if area_m2 else None
    city["median_household_income"] = median_income
    city["foreign_born_population"] = foreign_born
    city["foreign_born_share"] = foreign_born / city["population"] if foreign_born is not None else None
    city["land_area_sq_mi"] = area_sq_mi
    city["population_density_sq_mi"] = city["population"] / area_sq_mi if area_sq_mi else None
    city["log_median_household_income"] = math.log(median_income) if median_income else None
    city["log_population_density"] = math.log(city["population_density_sq_mi"]) if city["population_density_sq_mi"] else None
    city["chinese_high_confidence_per_100k"] = (
        city["chinese_high_confidence"] / city["population"] * 100_000
    )
    records = features_by_city[geoid]
    count = len(records)
    cuisine_tag = sum(r.get("classification_basis") == "cuisine tag" for r in records)
    name_based = sum(r.get("classification_basis") == "name keyword" for r in records)
    address = sum(bool(r.get("address")) for r in records)
    website = sum(bool(r.get("website")) for r in records)
    named = sum(bool(r.get("name") and r.get("name") != "Unnamed eatery") for r in records)
    candidate_count = city.get("candidate_osm_objects") or 0
    audit = {
        "label": city["label"],
        "state": city["state"],
        "city_geoid": geoid,
        "classified_records": count,
        "candidate_osm_objects": candidate_count,
        "classified_share_of_candidates": count / candidate_count if candidate_count else None,
        "cuisine_tag_records": cuisine_tag,
        "cuisine_tag_share": cuisine_tag / count if count else None,
        "name_keyword_records": name_based,
        "name_keyword_share": name_based / count if count else None,
        "records_with_address": address,
        "address_completeness": address / count if count else None,
        "records_with_website": website,
        "website_completeness": website / count if count else None,
        "named_records": named,
        "name_completeness": named / count if count else None,
    }
    audit_rows.append(audit)
    city.update(
        {
            "osm_cuisine_tag_share": audit["cuisine_tag_share"],
            "osm_address_completeness": audit["address_completeness"],
            "osm_website_completeness": audit["website_completeness"],
        }
    )

correlation_specs = [
    ("chinese_share", "chinese_per_100k"),
    ("asian_share", "chinese_per_100k"),
    ("foreign_born_share", "chinese_per_100k"),
    ("median_household_income", "chinese_per_100k"),
    ("population_density_sq_mi", "chinese_per_100k"),
    ("chinese_share", "chinese_high_confidence_per_100k"),
    ("foreign_born_share", "chinese_share"),
]
correlations = [pearson_summary(cities, x, y) for x, y in correlation_specs]
without_bellevue = [row for row in cities if row["label"] != "Bellevue, WA"]
sensitivity = {
    "chinese_share_vs_chinese_per_100k_without_bellevue": pearson_summary(
        without_bellevue, "chinese_share", "chinese_per_100k"
    ),
    "high_confidence_only": pearson_summary(
        cities, "chinese_share", "chinese_high_confidence_per_100k"
    ),
}

model = ols_hc3(
    cities,
    "chinese_per_100k",
    [
        "chinese_share",
        "foreign_born_share",
        "log_median_household_income",
        "log_population_density",
    ],
)

state_rows = []
for state in sorted({row["state"] for row in cities}):
    subset = [row for row in cities if row["state"] == state]
    state_rows.append(
        {
            "state": state,
            "cities": len(subset),
            "mean_chinese_per_100k": float(np.mean([r["chinese_per_100k"] for r in subset])),
            "median_chinese_per_100k": float(np.median([r["chinese_per_100k"] for r in subset])),
            "mean_chinese_share": float(np.mean([r["chinese_share"] for r in subset])),
            "mean_foreign_born_share": float(np.mean([r["foreign_born_share"] for r in subset])),
        }
    )

duplicate_ids = sum(count - 1 for count in Counter(global_ids).values() if count > 1)
overall_audit = {
    "records": len(global_ids),
    "duplicate_osm_type_id_rows": duplicate_ids,
    "cuisine_tag_share": sum(r["cuisine_tag_records"] for r in audit_rows) / len(global_ids),
    "name_keyword_share": sum(r["name_keyword_records"] for r in audit_rows) / len(global_ids),
    "address_completeness": sum(r["records_with_address"] for r in audit_rows) / len(global_ids),
    "website_completeness": sum(r["records_with_website"] for r in audit_rows) / len(global_ids),
    "name_completeness": sum(r["named_records"] for r in audit_rows) / len(global_ids),
}

extended_payload = {
    **{k: v for k, v in payload.items() if k != "cities"},
    "extended_as_of": "2026-11-21",
    "additional_sources": {
        "median_household_income": income_url,
        "foreign_born_population": birth_url,
        "land_area": "2024 Census TIGER/Line incorporated-place ALAND field",
    },
    "cities": cities,
}
with (OUT / "city_summary_extended.json").open("w", encoding="utf-8") as handle:
    json.dump(extended_payload, handle, indent=2)

# Join the new city-level variables back onto the city polygons used by the
# public map.  Geometry remains unchanged; only the properties are extended.
city_geometry = read_json(PROCESSED / "city_boundaries.geojson")
city_by_geoid = {row["geoid"]: row for row in cities}
for feature in city_geometry["features"]:
    geoid = feature["properties"].get("geoid")
    if geoid in city_by_geoid:
        feature["properties"].update(city_by_geoid[geoid])
with (OUT / "cities_extended.geojson").open("w", encoding="utf-8") as handle:
    json.dump(city_geometry, handle, separators=(",", ":"))

context_fields = [
    "geoid",
    "median_household_income",
    "foreign_born_population",
    "foreign_born_share",
    "land_area_sq_mi",
    "population_density_sq_mi",
    "chinese_high_confidence_per_100k",
    "osm_cuisine_tag_share",
    "osm_address_completeness",
    "osm_website_completeness",
]
with (OUT / "city_context.json").open("w", encoding="utf-8") as handle:
    json.dump(
        {
            "updated": "2026-11-21",
            "cities": [
                {key: row.get(key) for key in context_fields}
                for row in cities
            ],
        },
        handle,
        separators=(",", ":"),
    )

city_fields = [
    "state", "name", "label", "geoid", "population", "asian_population", "chinese_population",
    "asian_share", "chinese_share", "median_household_income", "foreign_born_population",
    "foreign_born_share", "land_area_sq_mi", "population_density_sq_mi", "chinese_eateries",
    "chinese_high_confidence", "chinese_name_based", "other_asian_eateries", "asian_eateries",
    "chinese_per_100k", "chinese_high_confidence_per_100k", "other_asian_per_100k",
    "chinese_share_of_asian_eateries", "candidate_osm_objects", "osm_cuisine_tag_share",
    "osm_address_completeness", "osm_website_completeness", "source_release", "query_status",
]
with (OUT / "city_summary_extended.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=city_fields)
    writer.writeheader()
    writer.writerows({key: row.get(key) for key in city_fields} for row in cities)

audit_fields = list(audit_rows[0])
with (OUT / "osm_validation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=audit_fields)
    writer.writeheader()
    writer.writerows(audit_rows)

analysis = {
    "analysis_as_of": "2026-11-21",
    "sample_size": len(cities),
    "sample_design": payload["selection_rule"],
    "correlations": correlations,
    "sensitivity": sensitivity,
    "exploratory_multivariable_model": model,
    "state_descriptives": state_rows,
    "osm_audit_overall": overall_audit,
    "interpretation_guardrails": [
        "Cities were selected for large Asian populations rather than sampled randomly.",
        "OSM counts are lower-bound observations and platform coverage may differ by city.",
        "The multivariable model is exploratory with only 30 cities and cannot establish causation.",
        "Foreign-born share and Chinese population share overlap conceptually and statistically.",
    ],
}
with (OUT / "socioeconomic_analysis.json").open("w", encoding="utf-8") as handle:
    json.dump(analysis, handle, indent=2)

print(json.dumps(analysis, indent=2))
