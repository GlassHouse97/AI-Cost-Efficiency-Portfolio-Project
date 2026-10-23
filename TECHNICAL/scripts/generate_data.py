"""Rebuild the fictional MRU source data. Contains solution spoilers.

Python 3.10+, standard library only. Run from any working directory.
Integer tokens are generated first. Charges are always tokens times stated rates.
"""
from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = 20261022
DEPARTMENTS = ["Content", "Creative", "Marketing Operations", "Analytics"]
EMPLOYEES = ["Avery Morgan", "Jordan Ellis", "Riley Chen", "Taylor Brooks",
             "Casey Rivera", "Morgan Reed", "Quinn Parker", "Jamie Patel"]
TASK_TYPES = {
    "Content": ["Write ad copy", "Draft email sequence", "Edit landing page"],
    "Creative": ["Develop concept brief", "Review creative variants", "Plan visual narrative"],
    "Marketing Operations": ["Build campaign plan", "Clean audience data", "Prepare launch checklist"],
    "Analytics": ["Analyze campaign results", "Summarize audience insights", "Check measurement plan"],
}
PRODUCTS = {"Content": "CopyStudio", "Creative": "CampaignChat",
            "Marketing Operations": "DataFlow", "Analytics": "InsightDesk"}
PRICES = [
    {"model": "Lite", "input_rate_usd_per_million": 10, "output_rate_usd_per_million": 30},
    {"model": "Pro", "input_rate_usd_per_million": 40, "output_rate_usd_per_million": 100},
]
CONFIG = {
    "C001": {"base": 24000, "actual": 14000, "prompts": 600, "pro_tasks": 12,
             "Lite": (20000000, 4000000), "Pro": (2000000, 1000000),
             "revenue": 25000, "other": 10000},
    "C002": {"base": 20000, "actual": 27000, "prompts": 1200, "pro_tasks": 30,
             "Lite": (20000000, 4000000), "Pro": (12000000, 6000000),
             "revenue": 20000, "other": 7500},
    "C003": {"base": 22000, "actual": 17200, "prompts": 720, "pro_tasks": 18,
             "Lite": (14000000, 3000000), "Pro": (4000000, 1500000),
             "revenue": 23000, "other": 9500},
    "C004": {"base": 26000, "actual": 21800, "prompts": 840, "pro_tasks": 24,
             "Lite": (10000000, 2000000), "Pro": (7000000, 3000000),
             "revenue": 27000, "other": 12000},
}
WORK_FIELDS = ["work_item_id", "completion_date", "campaign_id", "department", "employee", "task_type",
               "baseline_hours", "actual_hours", "rework_hours", "issue_tag", "brief_changed", "prompt_template_used"]
USAGE_FIELDS = ["usage_id", "usage_date", "work_item_id", "campaign_id", "product", "model", "input_tokens", "output_tokens", "prompt_reason"]
QUICK_FIELDS = ["work_item_id", "completion_date", "campaign", "department", "employee", "product", "model", "task_type",
                "prompt_count", "input_tokens", "output_tokens", "input_rate_usd_per_million", "output_rate_usd_per_million",
                "baseline_hours", "actual_hours", "rework_hours", "issue_tag"]


def allocate(total: int, weights: list[float], minimum: int = 0) -> list[int]:
    """Largest-remainder apportionment preserves exact integer totals."""
    available = total - minimum * len(weights)
    if available < 0 or not weights or min(weights) <= 0:
        raise ValueError("Invalid allocation")
    shares = [available * weight / sum(weights) for weight in weights]
    values = [int(value) + minimum for value in shares]
    remainder = total - sum(values)
    order = sorted(range(len(weights)), key=lambda i: (shares[i] % 1, -i), reverse=True)
    for i in order[:remainder]:
        values[i] += 1
    assert sum(values) == total
    return values


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build() -> dict[str, list[dict]]:
    rng = random.Random(SEED)
    work, usage, campaigns = [], [], []
    days = [date(2026, 9, day) for day in range(1, 31)
            if date(2026, 9, day).weekday() < 5 and day != 7]
    for campaign_no, (campaign_id, config) in enumerate(CONFIG.items(), 1):
        campaigns.append({"campaign_id": campaign_id, "campaign_name": f"Campaign {campaign_no}",
                          "campaign_revenue_usd": config["revenue"], "other_campaign_cost_usd": config["other"]})
        pro_indices = set(rng.sample(range(60), config["pro_tasks"]))
        baseline = allocate(config["base"], [rng.uniform(0.55, 1.5) for _ in range(60)], minimum=100)
        ratios = []
        for index in range(60):
            if campaign_id == "C001":
                ratio = rng.uniform(1.15, 1.5) if index < 8 else rng.uniform(0.3, 0.65)
            elif campaign_id == "C002":
                ratio = rng.uniform(0.35, 0.65) if index < 10 else rng.uniform(1.1, 1.9)
            else:
                ratio = rng.uniform(0.4, 1.25)
            ratios.append(ratio)
        actual = allocate(config["actual"], [base * ratio for base, ratio in zip(baseline, ratios)], minimum=25)
        prompt_counts = allocate(config["prompts"], [rng.uniform(0.6, 1.45) * (1.5 if ratios[i] > 1 else 1)
                                                    for i in range(60)], minimum=3)
        campaign_tasks = []
        for index in range(60):
            task_id = f"W{len(work) + 1:04d}"
            employee_index = (index + campaign_no - 1) % 8
            department = DEPARTMENTS[employee_index // 2]
            model = "Pro" if index in pro_indices else "Lite"
            # Most tasks use the department's primary product, with realistic cross-use.
            product = PRODUCTS[department] if rng.random() < 0.72 else rng.choice(list(PRODUCTS.values()))
            underperforming = actual[index] >= baseline[index]
            template = rng.random() < (0.84 if campaign_id == "C001" else 0.30 if campaign_id == "C002" else 0.60)
            brief_changed = rng.random() < (0.45 if campaign_id == "C002" else 0.15)
            if brief_changed:
                issue = "Brief changed"
            elif rng.random() < (0.7 if underperforming else 0.2):
                issue = rng.choice(["Unclear prompt", "Data problem"])
            else:
                issue = "None"
            fraction = rng.uniform(0.2, 0.48) if campaign_id == "C002" else rng.uniform(0.02, 0.20)
            if issue == "None":
                fraction *= 0.5
            rework = round(actual[index] * fraction)
            end_index = 3 + ((index * 7 + campaign_no * 3) % (len(days) - 3))
            row = {"work_item_id": task_id, "completion_date": days[end_index].isoformat(),
                   "campaign_id": campaign_id, "department": department, "employee": EMPLOYEES[employee_index],
                   "task_type": TASK_TYPES[department][index % 3], "baseline_hours": baseline[index] / 100,
                   "actual_hours": actual[index] / 100, "rework_hours": rework / 100, "issue_tag": issue,
                   "brief_changed": "Yes" if brief_changed else "No", "prompt_template_used": "Yes" if template else "No"}
            work.append(row)
            campaign_tasks.append({"row": row, "model": model, "product": product,
                                   "count": prompt_counts[index], "end_index": end_index})
        for model in ["Lite", "Pro"]:
            selected = [task for task in campaign_tasks if task["model"] == model]
            input_totals = allocate(config[model][0], [task["count"] * rng.uniform(0.6, 1.6) for task in selected], 1000)
            output_totals = allocate(config[model][1], [task["count"] * rng.uniform(0.6, 1.6) for task in selected], 500)
            for task, total_input, total_output in zip(selected, input_totals, output_totals):
                count = task["count"]
                row = task["row"]
                inputs = allocate(total_input, [rng.uniform(0.5, 1.5) for _ in range(count)], 100)
                outputs = allocate(total_output, [rng.uniform(0.4, 1.6) for _ in range(count)], 50)
                correction_share = 0.42 if campaign_id == "C002" else 0.12 if campaign_id == "C001" else 0.23
                corrections = max(0, min(count - 1, round((count - 1) * correction_share * rng.uniform(0.6, 1.4))))
                reasons = ["First attempt"] + ["Correction"] * corrections + ["Followup"] * (count - 1 - corrections)
                # First attempt is earliest; later prompts alternate between followups and corrections.
                tail = reasons[1:]
                rng.shuffle(tail)
                reasons = reasons[:1] + tail
                for prompt_index, (input_tokens, output_tokens, reason) in enumerate(zip(inputs, outputs, reasons)):
                    day_index = task["end_index"] - 3 + min(3, prompt_index * 4 // count)
                    usage.append({"usage_id": f"U{len(usage) + 1:05d}", "usage_date": days[day_index].isoformat(),
                                  "work_item_id": row["work_item_id"], "campaign_id": campaign_id,
                                  "product": task["product"], "model": model, "input_tokens": input_tokens,
                                  "output_tokens": output_tokens, "prompt_reason": reason})
    return {"work_log": work, "ai_usage": usage, "model_pricing": PRICES, "campaigns": campaigns}


def main() -> None:
    data = build()
    usage_by_task = defaultdict(list)
    for row in data["ai_usage"]:
        usage_by_task[row["work_item_id"]].append(row)
    price_lookup = {row["model"]: row for row in PRICES}
    # Keep the completed demonstration clean. Only learner exports contain the specified defects.
    raw_work = [dict(row) for row in data["work_log"]]
    for index in [4, 17, 36, 61, 86, 109, 132, 179, 203, 228]:
        raw_work[index]["department"] = "  " + raw_work[index]["department"].lower() + " "
    quick = []
    for row in raw_work[:120]:
        prompts = usage_by_task[row["work_item_id"]]
        rates = price_lookup[prompts[0]["model"]]
        item = {key: row[key] for key in ["work_item_id", "completion_date", "department", "employee", "task_type",
                                        "baseline_hours", "actual_hours", "rework_hours", "issue_tag"]}
        item.update(campaign=f"Campaign {int(row['campaign_id'][1:])}", product=prompts[0]["product"],
                    model=prompts[0]["model"], prompt_count=len(prompts),
                    input_tokens=sum(p["input_tokens"] for p in prompts), output_tokens=sum(p["output_tokens"] for p in prompts),
                    input_rate_usd_per_million=rates["input_rate_usd_per_million"],
                    output_rate_usd_per_million=rates["output_rate_usd_per_million"])
        quick.append(item)
    duplicate_indices = [17, 86]
    quick += [dict(quick[index]) for index in duplicate_indices]
    raw_work += [dict(raw_work[index]) for index in duplicate_indices]
    write_csv(ROOT / "DATA/TRACKS/quick-challenge/mru_quick_challenge.csv", quick, QUICK_FIELDS)
    write_csv(ROOT / "DATA/TRACKS/portfolio-project/work_log.csv", raw_work, WORK_FIELDS)
    write_csv(ROOT / "DATA/TRACKS/portfolio-project/ai_usage.csv", data["ai_usage"], USAGE_FIELDS)
    write_csv(ROOT / "DATA/TRACKS/portfolio-project/model_pricing.csv", PRICES, list(PRICES[0]))
    write_csv(ROOT / "DATA/TRACKS/portfolio-project/campaigns.csv", data["campaigns"], list(data["campaigns"][0]))
    demo = ROOT / "TECHNICAL/dashboard/demo-data.json"
    demo.parent.mkdir(parents=True, exist_ok=True)
    demo.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Generated seed {SEED}: 122 quick rows, 242 work rows, {len(data['ai_usage'])} prompt rows, 240 clean demo tasks.")


if __name__ == "__main__":
    main()
