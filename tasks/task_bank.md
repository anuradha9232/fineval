# Task Bank

Seven evaluation tasks across two finance datasets. Each task is an adversarial prompt designed to be hard in a specific, known way - a place where models predictably slip. Each has a verified ground-truth answer (`datasets/ground_truth.json`) and a weighted rubric (`rubrics/<id>.json`).

| ID | Title | Dataset | Type | Targets this weakness |
|---|---|---|---|---|
| [T01](T01.md) | What drives market cap - revenue or profit? | company_financials | closed | Confusing which of two similar correlations is stronger |
| [T02](T02.md) | Average net margin and sector ranking | company_financials | closed | Averaging a ratio the wrong way (mean of ratios vs ratio of totals) |
| [T03](T03.md) | Valuation drivers | company_financials | open | Over-claiming: correlation stated as causation |
| [T04](T04.md) | Quarter-on-quarter growth by sector | segment_quarterly | closed | Growth as absolute difference instead of percentage |
| [T05](T05.md) | FY revenue and share table | segment_quarterly | spreadsheet | Totals that don't reconcile; shares that don't sum to 100% |
| [T06](T06.md) | Anomaly detection | segment_quarterly | open | Missing the real outlier, or over-reacting to it |
| [T07](T07.md) | Largest sector and revenue concentration | segment_quarterly | closed | Concentration/contribution arithmetic |

## Coverage

- **Prompt types:** 4 closed, 2 open, 1 spreadsheet-output.
- **Skills probed:** data cleaning, descriptive statistics, correlation, growth/variance, aggregation, anomaly detection, and grounded reasoning.
- **Failure modes:** each task maps to at least one entry in [`../docs/failure-taxonomy.md`](../docs/failure-taxonomy.md).

## How a task is structured

Every task file contains:
1. The **prompt** given to the model (natural language).
2. **Metadata** - dataset, type, and the weakness it targets.
3. A pointer to the **verified answer** and the **rubric**.
