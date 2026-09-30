# Rubric Schema

Each rubric is a JSON file in `rubrics/` named by task id (e.g. `T01.json`). Keeping rubrics as structured data — not prose — is what lets the scoring engine apply them mechanically and reproducibly.

## Structure

```json
{
  "task_id": "T01",
  "task_title": "What drives market cap — revenue or profit?",
  "dataset": "company_financials.csv",
  "prompt_type": "closed",
  "criteria": [
    {
      "id": "P1",
      "type": "positive",
      "weight": 15,
      "category": "accuracy",
      "text": "States that the average revenue ... is approximately Rs 1,435 crore."
    },
    {
      "id": "N1",
      "type": "negative",
      "weight": -40,
      "category": "accuracy",
      "text": "Reports the two correlations as roughly equal, or states that revenue is the stronger predictor."
    }
  ]
}
```

## Fields

| Field | Meaning |
|---|---|
| `task_id` | Matches the task file and the judgment keys |
| `prompt_type` | `closed`, `open`, or `spreadsheet` |
| `criteria[].id` | Short id (`P#` positive, `N#` negative, `S#` spot check) |
| `criteria[].type` | `positive` or `negative` (redundant with the weight's sign, kept for readability) |
| `criteria[].weight` | Signed integer. Positive criteria add; negative criteria subtract |
| `criteria[].category` | `accuracy`, `reasoning`, `instruction-following`, etc. |
| `criteria[].text` | The self-contained criterion, scorable pass/fail on its own |

## Rules the rubrics follow

- Each criterion is **atomic** (one idea), **self-contained** (the answer is in the text), and **objective** (pass/fail without opinion).
- Positive criteria carry the **required results**; the highest weights go on the results that matter most (accuracy over formatting).
- Negative criteria target **predictable mistakes**, and never exceed the absolute weight of their matching positive criterion.
- A negative criterion is written in positive language — the minus sign carries the penalty.

These are the same principles documented in the companion [evaluation-rubric-library](https://github.com/anuradha9232/evaluation-rubric-library); FinEval is where they're applied inside a running system.
