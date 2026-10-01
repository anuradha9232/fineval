# Model-Failure Taxonomy

The recurring ways models fail on finance data-analysis tasks, grouped by type. Each task in the bank is built to expose at least one of these, and each maps to negative criteria in the rubrics. Naming failure modes this way is what turns scattered "this answer is wrong" observations into a reusable checklist.

## 1. Calculation-method errors

The arithmetic runs, but the wrong method was used - so the number looks plausible and the error hides.

| Failure | Example | Task | Rubric |
|---|---|---|---|
| Averaging a ratio wrongly | Reporting ratio-of-totals (13.3%) as the average of per-company margins (14.0%) | T02 | T02.N1 |
| Absolute vs percentage change | Reporting growth as a rupee difference instead of a % change | T04 | T04.N2 |
| Totals that don't reconcile | FY total that isn't the sum of the parts | T05 | T05.N1 |
| Shares that don't sum to 100% | Percentage shares that add to 96% or 104% | T05 | T05.N2 |

## 2. Comparison / ranking errors

The model computes values but draws the wrong comparison between them.

| Failure | Example | Task | Rubric |
|---|---|---|---|
| Flipping which of two correlations is stronger | Saying revenue predicts market cap better than profit | T01 | T01.N1 |
| Naming the wrong extreme | Wrong highest-margin sector, or wrong declining sector | T02, T04 | T02.N2, T04.N1 |

## 3. Reasoning / over-claiming errors

The numbers are right but the interpretation over-reaches - often the most consequential, because a decision-maker may act on the sentence.

| Failure | Example | Task | Rubric |
|---|---|---|---|
| Correlation stated as causation | "Profit *causes* higher market cap" | T01, T03 | T01.N2, T03.N1 |
| Over-generalisation | Treating a 120-company snapshot as a universal rule | T03 | T03.N2 |
| Over-reaction to an outlier | Declaring the whole business in decline from one bad quarter | T06 | T06.N2 |

## 4. Detection / omission errors

The model misses something that is actually in the data.

| Failure | Example | Task | Rubric |
|---|---|---|---|
| Missing the real anomaly | Flagging a normal sector, or nothing, instead of the true outlier | T06 | T06.N1 |

## How to use this

When designing a new task, pick a failure mode from this list and build the prompt so a model is likely to fall into it - then write a negative criterion that catches it. When a new failure shows up in practice that isn't here, add it, and add a criterion for it. The taxonomy and the rubrics grow together.
