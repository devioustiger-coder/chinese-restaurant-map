# Platform and registry assessment

Updated November 22, 2026

## Purpose and method

This audit asks whether the OpenStreetMap-derived restaurant sample misses businesses that are readily visible in other sources. It compares only the first visible ranked public results for Chinese-restaurant searches in Bellevue, Seattle, and San Jose. Results outside the city or with an ambiguous/non-Chinese category were excluded before name-and-address matching. Selected omissions were then checked against official county food-facility records.

This is an illustrative, nonrandom pilot. It is not a capture-recapture estimate, an estimate of total platform coverage, or a complete restaurant census.

## Pilot result

- 51 visible results were reviewed; three were excluded, leaving 48 in-scope result rows.
- 32 of 48 result rows had a corresponding OSM restaurant record (66.7%).
- Three additional result rows were present in OSM but outside the project's strict Chinese category because the cuisine tag was Taiwanese.
- The highest apparent Yelp presence was in Seattle (10 of 10). The lowest source-city presence was Google Maps in San Jose (3 of 7).
- These rates should not be compared as population estimates because rankings are nonrandom and businesses repeat across platforms.

## Source decisions

| Source | Useful for | Main limitation | Project decision |
|---|---|---|---|
| OpenStreetMap | Reproducible locations, tags, and city-boundary analysis | Uneven completeness and inconsistent cuisine tagging | Keep as the baseline and label counts as lower-bound samples |
| Yelp | Finding likely omissions and observing rating/review-count snapshots | Search is not strictly city bounded; reviewed businesses only; API storage/analysis restrictions | Use only for documented spot checks unless research permission or licensing is obtained |
| Google Maps / Places | Finding likely omissions; place IDs; ratings, hours, price, and accessibility fields | Bulk scraping and long-term storage restrictions; paid API | Use for spot checks and identifiers, not the archived analytical dataset |
| Overture Maps Places | Large open place dataset independent of OSM, with names, categories, addresses, and existence confidence | Requires its own matching and category-cleaning workflow | Recommended next cross-check for all 30 cities |
| County food-facility registries | Official evidence of establishment presence and recency | Legal/permit names can differ; no cuisine classification | Use to validate Bellevue, Seattle, and San Jose candidates |
| Tripadvisor Content API | Location and review-related fields | Academic research is not an approved use | Do not use for this project |

## Confirmed examples

- Bellevue: Xiang House and the Bellevue Supreme Dumplings location appeared in King County food-establishment records but were absent from the OSM sample.
- Seattle: Blue Willow appeared in King County food-establishment records but was absent from the OSM sample.
- San Jose: Special Noodle, Golden House Chinese Restaurant, New Sam Kee Restaurant, China Chen, and Yummy Kitchen appeared in Santa Clara County's food-facility inventory but were absent from the OSM sample.
- Taxonomy issue: Bellevue's Din Tai Fung and Facing East were present in OSM but tagged Taiwanese, so a strict `cuisine=chinese` rule excluded them from the Chinese count.

## What this changes

The city-level correlation remains a valid relationship within the assembled OSM sample, but its restaurant counts should not be described as complete city totals. Cross-city differences can partly reflect source coverage and taxonomy, especially for San Jose. The three case studies should therefore triangulate OSM with official registries and commercial/mobility/community evidence.

## Recommended next validation step

1. Match Overture Places to OSM for all 30 cities using city boundaries and normalized names/addresses.
2. For Bellevue, Seattle, and San Jose, match the combined candidate list to county food-facility registries and record opening/inspection recency.
3. Draw a fixed, stratified manual validation sample per city rather than relying on ranked first-page results.
4. Report source-specific precision/recall uncertainty and repeat the city-level correlation with corrected or bounded counts.

## Source links

- [Yelp Business Search documentation](https://docs.developer.yelp.com/reference/v3_business_search)
- [Yelp Places API FAQ](https://docs.developer.yelp.com/docs/faq)
- [Google Maps Platform policies](https://developers.google.com/maps/terms)
- [Google Places policies](https://developers.google.com/maps/documentation/places/web-service/policies)
- [Overture Maps Places](https://docs.overturemaps.org/guides/places/)
- [King County Food Establishment Inspection Data](https://data.kingcounty.gov/Health-Wellness/Food-Establishment-Inspection-Data/f29f-zza5)
- [Santa Clara County Food Facility Inspections](https://data.sccgov.org/Health/Food-Facility-Inspections-v2/vuw7-jmjk)
- [Tripadvisor Content API](https://tripadvisor-content-api.readme.io/reference/overview)
