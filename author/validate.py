"""Independent source reconciliation. AUTHOR FILE: emits solution spoilers.

Does not import the generator or read saved check totals as input. Decimal math
keeps prompt costs exact; human time is summed from deduplicated tasks once.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = Decimal
DEPARTMENTS = {name.lower(): name for name in ["Content", "Creative", "Marketing Operations", "Analytics"]}
EXPECTED_PRICES = {"Lite": (10, 30), "Pro": (40, 100)}
EXPECTED_FOCAL = {
    "C001": {"input_tokens": 22000000, "output_tokens": 5000000, "baseline_hours": D("240"),
             "actual_hours": D("140"), "ai_cost_usd": D("500"), "net_ai_value_usd": D("4500"),
             "ai_roi_pct": D("900"), "campaign_result_usd": D("7500")},
    "C002": {"input_tokens": 32000000, "output_tokens": 10000000, "baseline_hours": D("200"),
             "actual_hours": D("270"), "ai_cost_usd": D("1400"), "net_ai_value_usd": D("-4900"),
             "ai_roi_pct": D("-350"), "campaign_result_usd": D("-2400")},
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def number(value) -> Decimal:
    result = D(str(value))
    require(result.is_finite(), "Numeric values must be finite")
    return result


def integer(value) -> int:
    result = number(value)
    require(result >= 0 and result == result.to_integral_value(), "Tokens/counts must be nonnegative integers")
    return int(result)


def normalize_department(value: str) -> str:
    key = value.strip().lower()
    require(key in DEPARTMENTS, f"Unknown department: {value!r}")
    return DEPARTMENTS[key]


def deduplicate(rows: list[dict], key: str) -> list[dict]:
    found = {}
    for row in rows:
        require(bool(row.get(key)), f"Missing {key}")
        if row[key] in found:
            require(row == found[row[key]], f"Conflicting duplicate {key}: {row[key]}")
        else:
            found[row[key]] = dict(row)
    return list(found.values())


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def load(root: Path = ROOT) -> dict:
    folder = root / "learners/portfolio-project"
    payload = {name: read_csv(folder / f"{name}.csv") for name in ["work_log", "ai_usage", "model_pricing", "campaigns"]}
    payload["quick"] = read_csv(root / "learners/quick-challenge/mru_quick_challenge.csv")
    payload["demo"] = json.loads((root / "dashboard/demo-data.json").read_text(encoding="utf-8"))
    return payload


def validate_data(payload: dict) -> dict:
    raw_work, raw_quick = payload["work_log"], payload["quick"]
    require(len(raw_work) == 242 and len(raw_quick) == 122, "Raw task export sizes")
    work, quick = deduplicate(raw_work, "work_item_id"), deduplicate(raw_quick, "work_item_id")
    require(len(work) == 240 and len(quick) == 120, "Clean task export sizes")
    raw_duplicates = {key for key, count in Counter(r["work_item_id"] for r in raw_work).items() if count > 1}
    quick_duplicates = {key for key, count in Counter(r["work_item_id"] for r in raw_quick).items() if count > 1}
    require(raw_duplicates == quick_duplicates and len(raw_duplicates) == 2, "Shared duplicate tasks")
    require(any(r["department"] != normalize_department(r["department"]) for r in work), "Department cleaning exercise present")
    for row in work:
        row["department"] = normalize_department(row["department"])
    for row in quick:
        row["department"] = normalize_department(row["department"])
    forbidden = {"total_tokens", "ai_cost_usd", "hours_saved", "time_value_usd", "net_ai_value_usd", "ai_roi_pct"}
    require(not any(forbidden.intersection(row) for name in ["work_log", "ai_usage", "quick"] for row in payload[name]), "No learner answer columns")
    prices = payload["model_pricing"]
    require(len(prices) == len(deduplicate(prices, "model")) == 2, "Unique model prices")
    price_map = {r["model"]: (integer(r["input_rate_usd_per_million"]), integer(r["output_rate_usd_per_million"])) for r in prices}
    require(price_map == EXPECTED_PRICES, "Fictional fixed price schedule")
    campaigns = payload["campaigns"]
    require(len(campaigns) == len(deduplicate(campaigns, "campaign_id")) == 4, "Unique campaigns")
    campaign_map = {row["campaign_id"]: row for row in campaigns}
    require(set(campaign_map) == {"C001", "C002", "C003", "C004"}, "Four campaign keys")
    for key, row in campaign_map.items():
        require(row["campaign_name"] == f"Campaign {int(key[1:])}", "Campaign display names")
        require(number(row["campaign_revenue_usd"]) >= 0 and number(row["other_campaign_cost_usd"]) >= 0, "Nonnegative campaign inputs")
    work_map = {row["work_item_id"]: row for row in work}
    require(len({r["employee"] for r in work}) == 8, "Eight fictional employees")
    employee_departments = defaultdict(set)
    for row in work:
        employee_departments[row["employee"]].add(row["department"])
        require(row["campaign_id"] in campaign_map, "Work campaign foreign key")
        completed = date.fromisoformat(row["completion_date"])
        require((completed.year, completed.month) == (2026, 9) and completed.weekday() < 5, "Completed September 2026 workdays")
        require(number(row["baseline_hours"]) >= 0 and number(row["actual_hours"]) >= 0, "Nonnegative time")
        require(D(0) <= number(row["rework_hours"]) <= number(row["actual_hours"]), "Rework is inside actual hours")
        require(row["brief_changed"] in {"Yes", "No"} and row["prompt_template_used"] in {"Yes", "No"}, "Yes/No flags")
        require(row["issue_tag"] in {"None", "Unclear prompt", "Brief changed", "Data problem"}, "Issue categories")
    require(all(len(values) == 1 for values in employee_departments.values()), "One department per employee")
    require(Counter(r["campaign_id"] for r in work) == {key: 60 for key in campaign_map}, "Sixty tasks per campaign")
    usage = payload["ai_usage"]
    require(2000 <= len(usage) <= 5000, "Prompt count range")
    require(len(usage) == len(deduplicate(usage, "usage_id")), "Usage IDs unique")
    task_usage = defaultdict(list)
    model_totals = defaultdict(lambda: {"input_tokens": 0, "output_tokens": 0})
    for row in usage:
        require(row["work_item_id"] in work_map, "Prompt work foreign key")
        task = work_map[row["work_item_id"]]
        require(row["campaign_id"] == task["campaign_id"], "Prompt/task campaign agreement")
        require(row["model"] in price_map, "Prompt model foreign key")
        require(row["product"] in {"CampaignChat", "CopyStudio", "DataFlow", "InsightDesk"}, "Product categories")
        require(row["prompt_reason"] in {"First attempt", "Followup", "Correction"}, "Prompt reason categories")
        used = date.fromisoformat(row["usage_date"])
        require((used.year, used.month) == (2026, 9) and used.weekday() < 5, "Usage September 2026 workdays")
        require(used <= date.fromisoformat(task["completion_date"]), "Prompt precedes task completion")
        for token in ["input_tokens", "output_tokens"]:
            model_totals[(row["campaign_id"], row["model"])][token] += integer(row[token])
        task_usage[row["work_item_id"]].append(row)
    require(set(task_usage) == set(work_map), "Every task has prompts")
    for task_id, prompts in task_usage.items():
        require(len({r["product"] for r in prompts}) == len({r["model"] for r in prompts}) == 1, "One product/model per task")
        require(sum(r["prompt_reason"] == "First attempt" for r in prompts) == 1, "One first attempt per task")
    focal_models = {("C001", "Lite"): (20000000, 4000000), ("C001", "Pro"): (2000000, 1000000),
                    ("C002", "Lite"): (20000000, 4000000), ("C002", "Pro"): (12000000, 6000000)}
    for key, expected in focal_models.items():
        require(tuple(model_totals[key].values()) == expected, f"Focal model token calibration {key}")
    totals = {}
    task_costs = {}
    for campaign_id, campaign in campaign_map.items():
        tasks = [r for r in work if r["campaign_id"] == campaign_id]
        prompts = [r for r in usage if r["campaign_id"] == campaign_id]
        input_cost = sum(D(integer(r["input_tokens"]) * price_map[r["model"]][0]) / D(1000000) for r in prompts)
        output_cost = sum(D(integer(r["output_tokens"]) * price_map[r["model"]][1]) / D(1000000) for r in prompts)
        cost = input_cost + output_cost
        baseline = sum(number(r["baseline_hours"]) for r in tasks)
        actual = sum(number(r["actual_hours"]) for r in tasks)
        saved = baseline - actual
        value = saved * 50 - cost
        totals[campaign_id] = {
            "tasks": len(tasks), "prompt_count": len(prompts),
            "input_tokens": sum(integer(r["input_tokens"]) for r in prompts),
            "output_tokens": sum(integer(r["output_tokens"]) for r in prompts),
            "input_cost_usd": input_cost, "output_cost_usd": output_cost, "ai_cost_usd": cost,
            "baseline_hours": baseline, "actual_hours": actual, "hours_saved": saved,
            "rework_hours": sum(number(r["rework_hours"]) for r in tasks),
            "time_value_usd": saved * 50, "net_ai_value_usd": value,
            "ai_roi_pct": value / cost * 100 if cost else None,
            "average_cost_per_prompt_usd": cost / len(prompts) if prompts else None,
            "campaign_revenue_usd": number(campaign["campaign_revenue_usd"]),
            "other_campaign_cost_usd": number(campaign["other_campaign_cost_usd"]),
            "campaign_result_usd": number(campaign["campaign_revenue_usd"]) - number(campaign["other_campaign_cost_usd"]) - actual * 50 - cost,
            "correction_prompts": sum(r["prompt_reason"] == "Correction" for r in prompts),
            "template_tasks": sum(r["prompt_template_used"] == "Yes" for r in tasks),
            "baseline_minus_20_net_value_usd": (baseline * D("0.8") - actual) * 50 - cost,
            "baseline_plus_20_net_value_usd": (baseline * D("1.2") - actual) * 50 - cost,
            "positive_net_value_tasks": 0, "negative_net_value_tasks": 0,
        }
        for task in tasks:
            task_prompts = task_usage[task["work_item_id"]]
            task_cost = sum((D(integer(r["input_tokens"]) * price_map[r["model"]][0]) +
                             D(integer(r["output_tokens"]) * price_map[r["model"]][1])) / D(1000000) for r in task_prompts)
            task_costs[task["work_item_id"]] = task_cost
            task_value = (number(task["baseline_hours"]) - number(task["actual_hours"])) * 50 - task_cost
            totals[campaign_id]["positive_net_value_tasks"] += task_value > 0
            totals[campaign_id]["negative_net_value_tasks"] += task_value < 0
        require(sum(task_costs[t["work_item_id"]] for t in tasks) == cost, "Task and prompt costs reconcile")
        for metric, expected in EXPECTED_FOCAL.get(campaign_id, {}).items():
            require(totals[campaign_id][metric] == expected, f"Focal target {campaign_id} {metric}")
    for row in quick:
        require(row["work_item_id"] in work_map, "Quick task foreign key")
        task = work_map[row["work_item_id"]]
        require(task["campaign_id"] in {"C001", "C002"}, "Quick focal campaigns")
        require(row["campaign"] == campaign_map[task["campaign_id"]]["campaign_name"], "Quick campaign name")
        for column in ["completion_date", "department", "employee", "task_type", "issue_tag"]:
            require(row[column] == task[column], f"Shared task attribute {column}")
        for column in ["baseline_hours", "actual_hours", "rework_hours"]:
            require(number(row[column]) == number(task[column]), f"Shared task time {column}")
        prompts = task_usage[row["work_item_id"]]
        require(integer(row["prompt_count"]) == len(prompts), "Quick prompt count")
        for token in ["input_tokens", "output_tokens"]:
            require(integer(row[token]) == sum(integer(p[token]) for p in prompts), f"Quick {token}")
        require(row["model"] == prompts[0]["model"] and row["product"] == prompts[0]["product"], "Quick model/product")
        rates = price_map[row["model"]]
        require((integer(row["input_rate_usd_per_million"]), integer(row["output_rate_usd_per_million"])) == rates, "Quick prices")
        quick_cost = (number(row["input_tokens"]) * rates[0] + number(row["output_tokens"]) * rates[1]) / 1000000
        require(quick_cost == task_costs[row["work_item_id"]], "Quick independent task cost")
    require({r["work_item_id"] for r in quick} == {r["work_item_id"] for r in work if r["campaign_id"] in {"C001", "C002"}}, "Identical focal population")
    for metric in ["prompt_count", "input_tokens", "output_tokens", "ai_cost_usd", "correction_prompts", "rework_hours"]:
        require(totals["C002"][metric] > totals["C001"][metric], f"C002 higher {metric}")
    require(totals["C001"]["template_tasks"] > totals["C002"]["template_tasks"], "C001 more templates")
    require(totals["C001"]["negative_net_value_tasks"] > 0 and totals["C002"]["positive_net_value_tasks"] > 0, "Within-campaign counterexamples")
    for metric in ["baseline_minus_20_net_value_usd", "baseline_plus_20_net_value_usd"]:
        require(totals["C001"][metric] > 0 and totals["C002"][metric] < 0, "Sensitivity signs hold")
    # Verify the published demo contains precisely the cleaned source records, no substituted answer totals.
    demo = payload["demo"]
    require(set(demo) == {"work_log", "ai_usage", "model_pricing", "campaigns"}, "Demo schema")
    for table, clean in [("work_log", work), ("ai_usage", usage), ("model_pricing", prices), ("campaigns", campaigns)]:
        require(len(demo[table]) == len(clean), f"Demo {table} population")
        for shown, source in zip(demo[table], clean):
            require(set(shown) == set(source), f"Demo {table} columns")
            for key, value in shown.items():
                require(not isinstance(value, bool), "Flags remain Yes/No strings")
                if isinstance(value, (int, float)):
                    require(number(value) == number(source[key]), f"Demo numeric {table}.{key}")
                else:
                    require(value == source[key], f"Demo text {table}.{key}")
    return {"seed": 20261022, "period": "2026-09", "status": "PASS", "clean_tasks": len(work),
            "raw_work_rows": len(raw_work), "raw_quick_rows": len(raw_quick), "usage_rows": len(usage),
            "campaigns": totals, "model_tokens": {f"{key[0]}_{key[1]}": value for key, value in model_totals.items()}}


def serialized(results: dict) -> str:
    return json.dumps(results, indent=2, default=lambda value: format(value, ".6f") if isinstance(value, D) else value) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-checks", action="store_true", help="Save independently calculated author/check_totals.json")
    args = parser.parse_args()
    results = validate_data(load())
    if args.write_checks:
        (ROOT / "author/check_totals.json").write_text(serialized(results), encoding="utf-8")
    print(serialized(results))


if __name__ == "__main__":
    main()
