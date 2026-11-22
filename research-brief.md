# Research brief: Chinese restaurant availability across selected West Coast cities

Updated November 21, 2026

## Research focus

Primary question: Across selected West Coast cities, how is Chinese population share associated with the number of sampled Chinese eateries per 100,000 residents?

Recommended explanatory question: After population composition is considered, which city-level factors—such as foreign-born share, income, density, and commercial context—may help explain differences in sampled Chinese-eatery availability?

Social-responsibility question: How might Chinese restaurants function as cultural and community infrastructure, and who may lack affordable, convenient, or welcoming access to these spaces?

## What the analysis shows

The sample contains 30 incorporated cities: the top 15 Washington, top 10 California, and top 5 Oregon cities by 2024 ACS Asian-alone population. Restaurant and fast-food records were obtained from OpenStreetMap and clipped to Census city boundaries.

- Chinese population share versus sampled Chinese eateries per 100,000: Pearson r = 0.676, p < .001, R² = 0.457; Spearman rho = 0.529, p = .003.
- Estimated bivariate slope: about 8.01 additional sampled Chinese eateries per 100,000 for a 10-percentage-point increase in Chinese population share.
- Cuisine-tag-only sensitivity: r = 0.688, p < .001.
- Excluding Bellevue: r = 0.636, p < .001.
- Asian population share versus rate: r = 0.388, p = .034, but Spearman rho = 0.287, p = .124. The result is weaker and sensitive to metric choice.
- Foreign-born share versus rate: r = 0.316, p = .089; no clear bivariate relationship.
- Median household income versus rate: Pearson r = 0.329, p = .075; Spearman rho = 0.450, p = .013. This suggests a possible monotonic pattern, but not a stable linear finding.
- Population density versus rate: Pearson r = 0.422, p = .020; Spearman rho = 0.152, p = .423. This discrepancy warns against a simple density conclusion.

An exploratory four-predictor model explains 58.7% of observed variance (adjusted R² = 0.521), but it uses only 30 purposefully selected cities. Chinese population share is the only clearly independent correlate. Foreign-born share overlaps strongly with Chinese share (r = 0.705), and the coefficient signs are not causal explanations.

## Focus-city comparison

| City | Chinese share | Sampled Chinese eateries | Per 100,000 | Foreign-born share | Median income | Density / sq mi |
|---|---:|---:|---:|---:|---:|---:|
| Bellevue, WA | 16.4% | 51 | 33.59 | 43.5% | $165,576 | 4,537 |
| Seattle, WA | 5.8% | 97 | 12.86 | 20.2% | $123,860 | 8,978 |
| San Jose, CA | 8.7% | 102 | 10.30 | 42.0% | $146,427 | 5,564 |

Bellevue's unusually high per-capita rate is a real descriptive observation in this dataset. It is not, by itself, evidence that income, immigration, or population density caused the difference.

## Feasibility of the four questions

| Question | Current feasibility | What is still needed |
|---|---|---|
| Population share and per-capita restaurant availability | Strong | Broader, systematically sampled cities and uncertainty analysis |
| Why Bellevue differs from Seattle and San Jose | Partial | Rents, commercial clusters, parking/transit, business openings/closures, interviews |
| Socioeconomic factors beyond population share | Exploratory and promising | Larger sample, prespecified variables, commercial land-use measures, stronger validation |
| Washington versus California and Oregon | Descriptive only | More balanced state samples and enough cities for defensible regional inference |

Nationwide expansion is technically feasible using TIGER/Line, ACS, and OSM, but it should be staged. A stratified 50–100-city pilot across regions would be more defensible than immediately processing every incorporated place because OSM coverage and city definitions vary widely.

## Data validation

Across 5,813 classified OSM records:

- duplicate OSM type/ID rows: 0;
- cuisine-tag classifications: 94.3%;
- name-keyword classifications: 5.7%;
- address completeness: 77.3%;
- website completeness: 46.0%;
- name completeness: 98.8%.

The cuisine-tag-only sensitivity test indicates that the main association is not created by the small name-keyword group. Yelp and Google Places were not used for wholesale validation because their APIs require credentials and billing or plan access, and platform terms constrain storage and analysis. A future study should use a licensed source or a small, documented manual match sample rather than scraping.

## Local context and inequality

The quantitative results are this project's original analysis. The points below are external context, not findings inferred from the correlations.

- Bellevue's 2023 retail study identifies affordability, access to capital, tenant improvement costs, landlord negotiation, displacement risk, and limited cross-cultural integration as concerns for multicultural retail. It also reports that some businesses outside Bellevue view the city as a place to reach a multicultural market. Source: [City of Bellevue Retail Study](https://bellevuewa.gov/city-government/departments/community-development/economic-development/retail-study).
- Seattle describes the Chinatown–International District as a cultural hub whose restaurants, markets, and events serve residents and visitors, while also documenting historic underinvestment, institutional racism, displacement pressure, safety concerns, and the need to preserve legacy businesses. Source: [City of Seattle CID community planning](https://seattle.gov/neighborhoods/community-connections/safety-and-capacity-building/chinatown-international-district).
- San Jose's AAPI business profiles connect business formation and expansion to refugee and immigrant histories, community concentration, malls, and commercial corridors. Source: [City of San José AAPI business spotlight](https://www.sanjoseca.gov/Home/Components/News/News/5159/4765).
- Portland's legacy-business work explicitly recognizes culturally specific restaurants and bars as vulnerable to involuntary displacement and important to cultural heritage. Source: [City of Portland legacy business project](https://www.portland.gov/bps/planning/historic-resources/legacy/news/2023/9/22/city-portland-receives-small-business).
- Research on online restaurant reviews finds that immigrant cuisines can be framed through stereotypes involving authenticity, exoticism, cost, hygiene, and status. This makes review text potentially useful but ethically sensitive evidence; ratings alone should not be treated as neutral measures of business quality. Source: [Luo, Gligorić, and Jurafsky](https://arxiv.org/abs/2307.07645).

## Lessons learned from the process

1. Geographic scale changes the question. Census tracts are useful for neighborhood context, but city scale better matches the fact that people cross neighborhood boundaries to eat and shop.
2. A large correlation between raw counts can mostly reflect city size. Per-capita rates and population shares are necessary for a more meaningful comparison.
3. Data-source completeness is part of the result. OSM should be described as a lower-bound sample, and classification rules need sensitivity tests.
4. Demographic association is not a mechanism. Explaining clustering requires business conditions, mobility, history, and community testimony.
5. “Chinese cuisine” is not the same as Chinese ownership, and “Asian” combines communities with different histories and needs.
6. Social responsibility cannot be reduced to map coverage. Belonging, affordability, disability access, language, displacement, and missing voices require qualitative and community-centered evidence.

## Next research steps

1. Keep the city-level demographic association as the baseline result.
2. Expand to a stratified multi-region city sample before claiming national patterns.
3. Add commercial context: retail space, rents, malls, job centers, transit, parking, and legacy business districts.
4. Conduct a small validation sample using a licensed platform or local business-license source.
5. Add interviews or community-partner evidence about belonging, displacement, and access.
6. Treat any AI ownership classification as a separate bias audit, never as verified ownership data.
