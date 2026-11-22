# Reproducible methods

The analysis uses 2024 ACS 5-year place-level demographics, 2024 TIGER/Line incorporated-place boundaries and land area, and OpenStreetMap restaurant/fast-food records observed November 4, 2026.

The public sample is purposive rather than random: the top 15 Washington, top 10 California, and top 5 Oregon incorporated cities by Asian-alone population, with the named focus cities retained.

Chinese classification is based first on OSM cuisine tags and second on a documented name-keyword rule. Cuisine-tag records are treated as high confidence; name-keyword records as medium confidence. All counts are lower-bound observations, and cuisine does not establish ownership.

The primary outcome is sampled Chinese eateries per 100,000 residents. The primary predictor is Chinese-alone population share. Pearson and Spearman correlations are both reported. Sensitivity tests exclude name-keyword classifications and exclude Bellevue. An exploratory OLS model uses standardized predictors and HC3 robust standard errors; it is descriptive and non-causal.

Run `extend_city_analysis.py` from a Python environment with NumPy and SciPy. The script reads the processed city dataset, downloads the relevant official 2024 ACS table-based summary files, joins TIGER/Line land area, audits OSM completeness, and writes the extended city data and statistical results.
