"""
score.py - FinEval scoring engine
---------------------------------
Scores one or more model responses against the task-bank rubrics and writes
per-model scorecards plus a two-model comparison.

Run:  python harness/score.py

Inputs:
  rubrics/*.json          - one rubric per task (weighted positive/negative criteria)
  responses/<model>.json  - a rater's pass/fail judgment of each criterion for that model

Outputs (written into reports/):
  scorecard_<model>.md    - detailed per-task and overall scorecard for each model
  comparison.md           - side-by-side comparison with the relative-advantage metric

Scoring rules (documented in docs/methodology.md):
  - A criterion marked present (true) contributes its signed weight
    (positive criteria add, negative criteria subtract).
  - A criterion marked absent (false) contributes 0.
  - A task score is floored at 0 (a task cannot score negative).
  - A task's maximum is the sum of its positive weights.
  - The overall score is total points / total maximum across all tasks.
"""

import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUBRICS_DIR = os.path.join(ROOT, "rubrics")
RESPONSES_DIR = os.path.join(ROOT, "responses")
REPORTS_DIR = os.path.join(ROOT, "reports")


def load_rubrics():
    rubrics = {}
    for path in sorted(glob.glob(os.path.join(RUBRICS_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            r = json.load(f)
        rubrics[r["task_id"]] = r
    return rubrics


def load_model(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def score_task(rubric, task_judgment):
    """Return the scored rows and totals for one task."""
    rows = []
    raw = 0
    max_pos = 0
    for c in rubric["criteria"]:
        if c["weight"] > 0:
            max_pos += c["weight"]
        met = bool(task_judgment.get(c["id"], False))
        pts = c["weight"] if met else 0
        raw += pts
        rows.append({
            "id": c["id"], "type": c["type"], "weight": c["weight"],
            "text": c["text"], "met": met, "points": pts,
        })
    score = max(raw, 0)  # floor a task at 0
    return {"rows": rows, "raw": raw, "score": score, "max_pos": max_pos}


def score_model(rubrics, model):
    judgments = model["judgments"]
    per_task = {}
    total_score = 0
    total_max = 0
    for tid in sorted(rubrics):
        res = score_task(rubrics[tid], judgments.get(tid, {}))
        per_task[tid] = res
        total_score += res["score"]
        total_max += res["max_pos"]
    pct = (total_score / total_max * 100) if total_max else 0.0
    return {"per_task": per_task, "total_score": total_score,
            "total_max": total_max, "pct": pct}


def write_scorecard(model, rubrics, scored):
    name = model["model"]
    lines = [f"# Scorecard - {name}", ""]
    lines.append(f"*{model.get('description', '')}*", )
    lines.append("")
    lines.append(f"**Overall: {scored['total_score']} / {scored['total_max']} "
                 f"= {scored['pct']:.1f}%**")
    lines.append("")

    for tid in sorted(rubrics):
        r = rubrics[tid]
        res = scored["per_task"][tid]
        lines.append(f"## {tid} - {r['task_title']}")
        lines.append("")
        lines.append(f"Score: **{res['score']} / {res['max_pos']}**"
                     + (f"  (raw {res['raw']}, floored to 0)" if res["raw"] < 0 else ""))
        lines.append("")
        lines.append("| Criterion | Type | Weight | Met? | Points |")
        lines.append("|---|---|---:|:---:|---:|")
        for row in res["rows"]:
            met = "yes" if row["met"] else "no"
            lines.append(f"| {row['id']} {row['text']} | {row['type']} | "
                         f"{row['weight']:+d} | {met} | {row['points']:+d} |")
        lines.append("")

    out = os.path.join(REPORTS_DIR, f"scorecard_{name}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return out


def relative_advantage(a, b):
    """OpenClaw-style relative advantage of model a over model b."""
    return (a - b) / a if a else 0.0


def write_comparison(models_scored, rubrics):
    # models_scored: list of (model_dict, scored_dict) sorted best-first
    lines = ["# Model Comparison", ""]
    lines.append("All models scored on the identical rubric set and weights.")
    lines.append("")

    # overall table
    lines.append("## Overall")
    lines.append("")
    lines.append("| Model | Score | Max | Percentage |")
    lines.append("|---|---:|---:|---:|")
    for m, s in models_scored:
        lines.append(f"| {m['model']} | {s['total_score']} | {s['total_max']} | {s['pct']:.1f}% |")
    lines.append("")

    if len(models_scored) >= 2:
        (ma, sa), (mb, sb) = models_scored[0], models_scored[1]
        adv = relative_advantage(sa["total_score"], sb["total_score"])
        lines.append(f"**Relative advantage of {ma['model']} over {mb['model']}: "
                     f"{adv*100:.1f}%**  "
                     f"= ({sa['total_score']} - {sb['total_score']}) / {sa['total_score']}")
        lines.append("")
        verdict = "clears" if adv >= 0.15 else "does not clear"
        lines.append(f"This {verdict} the 15% relative-advantage bar used to confirm a task "
                     f"meaningfully separates a strong model from a weak one.")
        lines.append("")

    # per-task table
    lines.append("## Per-task percentage")
    lines.append("")
    header = "| Task | " + " | ".join(m["model"] for m, _ in models_scored) + " |"
    sep = "|---|" + "|".join(["---:"] * len(models_scored)) + "|"
    lines.append(header)
    lines.append(sep)
    for tid in sorted(rubrics):
        cells = []
        for _, s in models_scored:
            res = s["per_task"][tid]
            pct = (res["score"] / res["max_pos"] * 100) if res["max_pos"] else 0
            cells.append(f"{pct:.0f}%")
        lines.append(f"| {tid} {rubrics[tid]['task_title']} | " + " | ".join(cells) + " |")
    lines.append("")

    out = os.path.join(REPORTS_DIR, "comparison.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return out


def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    rubrics = load_rubrics()

    scored_all = []
    for path in sorted(glob.glob(os.path.join(RESPONSES_DIR, "*.json"))):
        model = load_model(path)
        scored = score_model(rubrics, model)
        write_scorecard(model, rubrics, scored)
        scored_all.append((model, scored))
        print(f"{model['model']:14s} {scored['total_score']:4d}/{scored['total_max']} "
              f"= {scored['pct']:5.1f}%")

    scored_all.sort(key=lambda ms: ms[1]["total_score"], reverse=True)
    if scored_all:
        write_comparison(scored_all, rubrics)

    if len(scored_all) >= 2:
        adv = relative_advantage(scored_all[0][1]["total_score"], scored_all[1][1]["total_score"])
        print(f"\nRelative advantage ({scored_all[0][0]['model']} over "
              f"{scored_all[1][0]['model']}): {adv*100:.1f}%")
    print(f"\nReports written to {REPORTS_DIR}")


if __name__ == "__main__":
    main()
