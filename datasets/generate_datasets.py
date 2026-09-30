"""
generate_datasets.py
---------------------
Builds the two datasets FinEval's task bank runs on, and computes the verified
ground-truth answers every rubric is checked against.

Run:  python datasets/generate_datasets.py

Outputs (written into datasets/):
  company_financials.csv   - 120 companies (sector, revenue, profit, market cap)
  segment_quarterly.csv    - quarterly revenue by sector for FY2024
  ground_truth.json        - the verified correct answers for all tasks

Everything is deterministic (fixed seed / fixed values), so anyone who runs this
gets exactly the same numbers the rubrics reference. The data is synthetic but
internally consistent, so the relationships the tasks ask about are real.
"""

import csv
import json
import os
import numpy as np

SEED = 42
N = 120
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "datasets")

SECTORS = ["IT Services", "Banking", "Pharma", "FMCG", "Automobile", "Energy"]

# Hand-set quarterly revenue (Rs crore) for dataset B. Values are chosen so the
# arithmetic is clean and one clear anomaly exists: Automobile Q4 drops sharply
# while every other sector grows.
QUARTERLY = {
    "IT Services": [420, 455, 470, 510],
    "Banking":     [380, 390, 405, 430],
    "Pharma":      [300, 310, 305, 330],
    "FMCG":        [260, 268, 275, 290],
    "Automobile":  [210, 205, 215, 150],   # <- Q4 anomaly
    "Energy":      [340, 355, 360, 385],
}


# ---------------------------------------------------------------- dataset A
def build_company_financials():
    rng = np.random.default_rng(SEED)
    sector = rng.choice(SECTORS, size=N)
    revenue = np.round(rng.lognormal(mean=7.0, sigma=0.9, size=N), 0)
    base_margin = {
        "IT Services": 0.22, "Banking": 0.18, "Pharma": 0.16,
        "FMCG": 0.14, "Automobile": 0.08, "Energy": 0.10,
    }
    margin = np.array([base_margin[s] for s in sector]) + rng.normal(0, 0.03, N)
    margin = np.clip(margin, 0.01, 0.40)
    net_profit = np.round(revenue * margin, 0)
    market_cap = np.round(
        net_profit * rng.uniform(9, 16, N) + revenue * 0.4
        + rng.normal(0, revenue.std() * 0.3, N), 0)
    market_cap = np.clip(market_cap, 50, None)

    rows = []
    for i in range(N):
        rows.append({
            "company": f"Company_{i+1:03d}",
            "sector": sector[i],
            "revenue_cr": int(revenue[i]),
            "net_profit_cr": int(net_profit[i]),
            "market_cap_cr": int(market_cap[i]),
        })
    with open(os.path.join(DATA, "company_financials.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company", "sector", "revenue_cr", "net_profit_cr", "market_cap_cr"])
        w.writeheader()
        w.writerows(rows)
    return rows


def ground_truth_A(rows):
    rev = np.array([r["revenue_cr"] for r in rows], float)
    prof = np.array([r["net_profit_cr"] for r in rows], float)
    mcap = np.array([r["market_cap_cr"] for r in rows], float)
    margins = prof / rev

    corr_rev = float(np.corrcoef(rev, mcap)[0, 1])
    corr_prof = float(np.corrcoef(prof, mcap)[0, 1])

    by_sector = {}
    for r in rows:
        by_sector.setdefault(r["sector"], []).append(r["net_profit_cr"] / r["revenue_cr"])
    sector_margin = {s: float(np.mean(v)) for s, v in by_sector.items()}
    top = max(sector_margin, key=sector_margin.get)
    low = min(sector_margin, key=sector_margin.get)

    return {
        "row_count": len(rows),
        "avg_revenue_cr": round(float(rev.mean()), 1),
        "avg_net_margin_pct": round(float(margins.mean() * 100), 2),
        "pearson_revenue_vs_marketcap": round(corr_rev, 3),
        "pearson_profit_vs_marketcap": round(corr_prof, 3),
        "highest_margin_sector": top,
        "highest_margin_sector_pct": round(sector_margin[top] * 100, 2),
        "lowest_margin_sector": low,
        "lowest_margin_sector_pct": round(sector_margin[low] * 100, 2),
    }


# ---------------------------------------------------------------- dataset B
def build_segment_quarterly():
    rows = []
    for sector, q in QUARTERLY.items():
        rows.append({
            "sector": sector,
            "q1_cr": q[0], "q2_cr": q[1], "q3_cr": q[2], "q4_cr": q[3],
        })
    with open(os.path.join(DATA, "segment_quarterly.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sector", "q1_cr", "q2_cr", "q3_cr", "q4_cr"])
        w.writeheader()
        w.writerows(rows)
    return rows


def ground_truth_B(rows):
    fy = {r["sector"]: r["q1_cr"] + r["q2_cr"] + r["q3_cr"] + r["q4_cr"] for r in rows}
    total = sum(fy.values())
    share = {s: round(v / total * 100, 2) for s, v in fy.items()}
    growth_q4_q3 = {r["sector"]: round((r["q4_cr"] - r["q3_cr"]) / r["q3_cr"] * 100, 2) for r in rows}
    largest = max(fy, key=fy.get)
    best_growth = max(growth_q4_q3, key=growth_q4_q3.get)
    worst_growth = min(growth_q4_q3, key=growth_q4_q3.get)

    return {
        "fy_total_cr": total,
        "fy_revenue_by_sector_cr": fy,
        "fy_share_by_sector_pct": share,
        "largest_sector_fy": largest,
        "largest_sector_fy_cr": fy[largest],
        "largest_sector_fy_share_pct": share[largest],
        "growth_q4_vs_q3_pct": growth_q4_q3,
        "highest_growth_sector": best_growth,
        "highest_growth_pct": growth_q4_q3[best_growth],
        "lowest_growth_sector": worst_growth,
        "lowest_growth_pct": growth_q4_q3[worst_growth],
        "anomaly": {
            "sector": "Automobile",
            "quarter": "Q4",
            "value_cr": 150,
            "note": "Automobile Q4 fell ~30% while every other sector grew; clear outlier.",
        },
    }


def main():
    os.makedirs(DATA, exist_ok=True)
    a = build_company_financials()
    b = build_segment_quarterly()
    gt = {
        "dataset_A_company_financials": ground_truth_A(a),
        "dataset_B_segment_quarterly": ground_truth_B(b),
    }
    with open(os.path.join(DATA, "ground_truth.json"), "w", encoding="utf-8") as f:
        json.dump(gt, f, indent=2)
    print("Wrote company_financials.csv, segment_quarterly.csv, ground_truth.json\n")
    print(json.dumps(gt, indent=2))


if __name__ == "__main__":
    main()
