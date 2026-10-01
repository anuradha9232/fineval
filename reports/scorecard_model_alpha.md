# Scorecard - model_alpha

*A strong model. Gets the core results and reasoning right; misses a few lower-weight details. Illustrative judgments authored by a human rater applying the rubrics.*

**Overall: 563 / 606 = 92.9%**

## T01 - What drives market cap - revenue or profit?

Score: **120 / 120**

| Criterion | Type | Weight | Met? | Points |
|---|---|---:|:---:|---:|
| P1 States that the average revenue across the 120 companies is approximately Rs 1,435 crore. | positive | +15 | yes | +15 |
| P2 Reports the Pearson correlation between revenue and market cap as approximately 0.92. | positive | +40 | yes | +40 |
| P3 Reports the Pearson correlation between net profit and market cap as approximately 0.97. | positive | +40 | yes | +40 |
| P4 States that net profit is more strongly correlated with market cap than revenue is. | positive | +25 | yes | +25 |
| N1 Reports the two correlations as roughly equal, or states that revenue is the stronger predictor of market cap. | negative | -40 | no | +0 |
| N2 States that profit causes market cap, presenting the correlation as a causal relationship. | negative | -20 | no | +0 |
| N3 Reports a correlation value above 1.0 or below -1.0. | negative | -15 | no | +0 |

## T02 - Average net margin and sector ranking

Score: **55 / 75**

| Criterion | Type | Weight | Met? | Points |
|---|---|---:|:---:|---:|
| P1 Reports the average net margin across the companies as approximately 14.0%. | positive | +30 | yes | +30 |
| P2 States that IT Services has the highest average net margin (approximately 21.3%). | positive | +25 | yes | +25 |
| P3 States that Automobile has the lowest average net margin (approximately 9.0%). | positive | +20 | no | +0 |
| N1 Computes the average margin as total profit divided by total revenue (about 13.3%) and labels it the average net margin. | negative | -25 | no | +0 |
| N2 Names a sector other than IT Services as the highest-margin sector. | negative | -15 | no | +0 |

## T03 - Valuation drivers (open-ended insight)

Score: **70 / 70**

| Criterion | Type | Weight | Met? | Points |
|---|---|---:|:---:|---:|
| P1 Concludes that net profit is the better predictor of market cap, grounded in the correlation values. | positive | +30 | yes | +30 |
| P2 Notes that both revenue and profit are strongly correlated with market cap, not only one of them. | positive | +20 | yes | +20 |
| P3 Gives a valid investor caution, such as association not implying causation, or the pattern being specific to this sample or period. | positive | +20 | yes | +20 |
| N1 Claims that profit causes market cap, presenting the correlation as a proven causal mechanism. | negative | -25 | no | +0 |
| N2 Treats this 120-company snapshot as a universal rule that holds for all companies and time periods. | negative | -15 | no | +0 |

## T04 - Quarter-on-quarter growth by sector

Score: **85 / 85**

| Criterion | Type | Weight | Met? | Points |
|---|---|---:|:---:|---:|
| P1 States that IT Services had the highest Q4-over-Q3 revenue growth (approximately 8.5%). | positive | +30 | yes | +30 |
| P2 States that Automobile had the lowest Q4-over-Q3 growth (approximately -30%). | positive | +35 | yes | +35 |
| P3 States that Automobile revenue declined in Q4 (negative growth). | positive | +20 | yes | +20 |
| N1 Names a sector other than Automobile as the weakest or declining sector. | negative | -30 | no | +0 |
| N2 Reports growth as an absolute rupee difference instead of a percentage change. | negative | -15 | no | +0 |

## T05 - FY revenue and share table (spreadsheet output)

Score: **93 / 101**

| Criterion | Type | Weight | Met? | Points |
|---|---|---:|:---:|---:|
| P1 States that total FY revenue across all sectors is Rs 8,018 crore. | positive | +30 | yes | +30 |
| P2 States that IT Services is the largest sector by FY revenue at Rs 1,855 crore. | positive | +25 | yes | +25 |
| P3 Reports the IT Services share of FY revenue as approximately 23.1%. | positive | +20 | yes | +20 |
| S1 Reports Banking FY revenue as Rs 1,605 crore (spot check). | positive | +8 | yes | +8 |
| S2 Reports Automobile FY revenue as Rs 780 crore (spot check). | positive | +8 | no | +0 |
| P4 Presents the result as a table sorted by FY revenue. | positive | +10 | yes | +10 |
| N1 Reports a total FY revenue other than Rs 8,018 crore. | negative | -20 | no | +0 |
| N2 Reports sector shares that do not sum to approximately 100%. | negative | -10 | no | +0 |

## T06 - Anomaly detection in quarterly revenue

Score: **70 / 70**

| Criterion | Type | Weight | Met? | Points |
|---|---|---:|:---:|---:|
| P1 Identifies Automobile Q4 as the anomaly or outlier in the data. | positive | +35 | yes | +35 |
| P2 Notes that Automobile Q4 fell about 30% while every other sector grew in Q4. | positive | +20 | yes | +20 |
| P3 Recommends investigating the cause of the Automobile Q4 drop before drawing conclusions. | positive | +15 | yes | +15 |
| N1 Identifies a sector or quarter other than Automobile Q4 as the main anomaly. | negative | -25 | no | +0 |
| N2 Concludes that the overall business is in decline based on this single quarterly drop. | negative | -15 | no | +0 |

## T07 - Largest sector and revenue concentration

Score: **70 / 85**

| Criterion | Type | Weight | Met? | Points |
|---|---|---:|:---:|---:|
| P1 States that IT Services is the largest sector by FY revenue. | positive | +30 | yes | +30 |
| P2 Reports IT Services FY revenue as Rs 1,855 crore. | positive | +20 | yes | +20 |
| P3 Reports the IT Services share of FY revenue as approximately 23.1%. | positive | +20 | yes | +20 |
| P4 States that the top two sectors (IT Services and Banking) together make up more than 40% of FY revenue. | positive | +15 | no | +0 |
| N1 Names a sector other than IT Services as the largest by FY revenue. | negative | -15 | no | +0 |

