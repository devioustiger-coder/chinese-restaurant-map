# West Coast Chinese Restaurant & City Context Map

An interactive city-level research map comparing sampled Chinese restaurant availability with Asian and Chinese population patterns across 30 selected cities in Washington, California, and Oregon. The revised map also adds median household income, foreign-born population share, population density, and OpenStreetMap completeness indicators.

The project includes a Bellevue census-tract detail view alongside the primary city-level comparison. Population estimates come from the 2024 ACS 5-year release, boundaries and land area come from 2024 TIGER/Line, and restaurant locations come from OpenStreetMap. Counts are lower-bound observations, not a complete business census, and cuisine classifications do not identify ownership.

## Headline findings

- Chinese population share and sampled Chinese eateries per 100,000 are positively associated across the 30 selected cities (Pearson r = 0.676, p < .001; Spearman rho = 0.529, p = .003).
- The relationship remains when only high-confidence cuisine-tag records are used (r = 0.688) and when Bellevue is excluded (r = 0.636).
- Median income, foreign-born share, and density are exploratory context variables. In a small multivariable model, Chinese population share is the only clearly independent correlate; the model is not causal.
- Bellevue has 51 sampled Chinese eateries (33.59 per 100,000), compared with Seattle's 97 (12.86 per 100,000) and San Jose's 102 (10.30 per 100,000).

## Research status

The data directly support city-level association and descriptive comparison questions. They do not establish why restaurants locate where they do, whether nearby residents are customers, whether communities have equal access, or whether a restaurant is Chinese-owned. Those questions require mobility, price, ownership, interview, and community evidence.

## Live map

Published with GitHub Pages.

## Files

- `index.html` — interactive Leaflet map
- `cities.geojson` — city boundaries and base demographic and restaurant statistics
- `city_context.json` — socioeconomic and OSM completeness fields joined to city polygons in the browser
- `asian_restaurants.geojson` — classified restaurant points
- `businesses.geojson` — original Bellevue business sample
- `tracts.geojson` — Bellevue census-tract context
- `research-brief.md` — findings, feasibility assessment, local context, and next steps
- `analysis/extend_city_analysis.py` — reproducible socioeconomic and validation analysis

