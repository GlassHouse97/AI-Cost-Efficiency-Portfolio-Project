"""Rebuild compact case-study evidence tables directly from the published CSVs.

Run validate_data.py first. This standard-library analysis independently prices
prompts with Decimal and aggregates them before counting each task's hours.
"""

from collections import defaultdict
import csv
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "DATA" / "portfolio-project"
OUTPUT = ROOT / "SOLUTION" / "outputs"
D = Decimal
ZERO = D(0)
RATE = D(50)


def read(name):
    with (SOURCE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name, rows):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: format(value, ".6f") if isinstance(value, D) else value
                             for key, value in row.items()})


def prepare():
    rates = {row["model"]: row for row in read("model_pricing.csv")}
    prompts = defaultdict(list)
    seen = set()
    for row in read("ai_usage.csv"):
        if row["usage_id"] in seen:
            raise ValueError("Repeated usage ID")
        seen.add(row["usage_id"])
        price = rates[row["model"]]
        for kind in ("input", "output"):
            row[f"{kind}_tokens"] = int(row[f"{kind}_tokens"])
            row[f"{kind}_cost_usd"] = (
                D(row[f"{kind}_tokens"]) * D(price[f"{kind}_rate_usd_per_million"])
                / D(1_000_000)
            )
        prompts[row["work_item_id"]].append(row)
    clean = {}
    for row in read("work_log.csv"):
        key = row["work_item_id"]
        if key in clean and row != clean[key]:
            raise ValueError(f"Conflicting duplicate task {key}")
        clean[key] = row
    tasks = []
    for key, original in clean.items():
        row = dict(original)
        usage = prompts.pop(key)
        if any(p["campaign_id"] != row["campaign_id"] for p in usage):
            raise ValueError(f"Campaign mismatch on {key}")
        for field in ("model", "product"):
            if len({p[field] for p in usage}) != 1:
                raise ValueError(f"Multiple {field} values on {key}")
            row[field] = usage[0][field]
        row["department"] = row["department"].strip().title()
        for field in ("baseline_hours", "actual_hours", "rework_hours"):
            row[field] = D(row[field])
        for field in ("input_tokens", "output_tokens", "input_cost_usd", "output_cost_usd"):
            row[field] = sum((p[field] for p in usage), 0)
        row["ai_cost_usd"] = row["input_cost_usd"] + row["output_cost_usd"]
        row["prompt_count"] = len(usage)
        row["correction_prompts"] = sum(p["prompt_reason"] == "Correction" for p in usage)
        row["hours_saved"] = row["baseline_hours"] - row["actual_hours"]
        row["net_ai_value_usd"] = row["hours_saved"] * RATE - row["ai_cost_usd"]
        tasks.append(row)
    if prompts:
        raise ValueError("Orphan prompt rows")
    return tasks


def summary(tasks):
    fields = ("input_tokens", "output_tokens", "input_cost_usd", "output_cost_usd",
              "ai_cost_usd", "prompt_count", "baseline_hours", "actual_hours",
              "hours_saved", "net_ai_value_usd", "rework_hours", "correction_prompts")
    result = {"tasks": len(tasks), **{field: sum((t[field] for t in tasks), 0) for field in fields}}
    cost = result["ai_cost_usd"]
    result["ai_roi_pct"] = result["net_ai_value_usd"] / cost * 100 if cost else "N/A"
    result["cost_per_prompt_usd"] = cost / result["prompt_count"] if result["prompt_count"] else "N/A"
    result["rework_share_pct"] = result["rework_hours"] / result["actual_hours"] * 100 if result["actual_hours"] else "N/A"
    result["template_tasks"] = sum(t["prompt_template_used"] == "Yes" for t in tasks)
    result["changed_brief_tasks"] = sum(t["brief_changed"] == "Yes" for t in tasks)
    result["positive_net_value_tasks"] = sum(t["net_ai_value_usd"] > ZERO for t in tasks)
    result["negative_net_value_tasks"] = sum(t["net_ai_value_usd"] < ZERO for t in tasks)
    return result


def groups(tasks, field, **prefix):
    return [{**prefix, field: label, **summary([t for t in tasks if t[field] == label])}
            for label in sorted({t[field] for t in tasks})]


def main():
    tasks = prepare()
    focal = [t for t in tasks if t["campaign_id"] in {"C001", "C002"}]
    scopes = {"all_four_campaigns": tasks, "focal_campaigns_1_2": focal}
    write("scope_summary.csv", [{"scope": name, **summary(rows)} for name, rows in scopes.items()])
    campaigns = {c["campaign_id"]: c for c in read("campaigns.csv")}
    campaign_rows = groups(tasks, "campaign_id")
    for row in campaign_rows:
        source = campaigns[row["campaign_id"]]
        row["campaign_revenue_usd"] = D(source["campaign_revenue_usd"])
        row["other_campaign_cost_usd"] = D(source["other_campaign_cost_usd"])
        row["actual_staff_cost_usd"] = row["actual_hours"] * RATE
        row["campaign_result_usd"] = (row["campaign_revenue_usd"] - row["other_campaign_cost_usd"]
                                      - row["actual_staff_cost_usd"] - row["ai_cost_usd"])
    write("campaign_summary.csv", campaign_rows)
    for field, filename in [("department", "department_summary.csv"), ("issue_tag", "issue_summary.csv")]:
        rows = []
        for name, subset in scopes.items():
            rows.extend(groups(subset, field, scope=name))
        for campaign_id in campaigns:
            rows.extend(groups([t for t in tasks if t["campaign_id"] == campaign_id], field, scope=campaign_id))
        write(filename, rows)
    for field in ("model", "product"):
        rows = []
        for campaign_id in campaigns:
            rows.extend(groups([t for t in tasks if t["campaign_id"] == campaign_id], field, campaign_id=campaign_id))
        write(f"{field}_summary.csv", rows)
    workflow = []
    for campaign_id in campaigns:
        subset = [t for t in tasks if t["campaign_id"] == campaign_id]
        for task_type in ["All task types", *sorted({t["task_type"] for t in subset})]:
            selected = subset if task_type == "All task types" else [t for t in subset if t["task_type"] == task_type]
            for dimension in ("prompt_template_used", "brief_changed"):
                for flag in ("No", "Yes"):
                    rows = [t for t in selected if t[dimension] == flag]
                    if rows:
                        workflow.append({"campaign_id": campaign_id, "task_type": task_type,
                                         "dimension": dimension, "flag": flag, **summary(rows)})
    write("workflow_summary.csv", workflow)
    sensitivity = []
    for row in campaign_rows:
        sensitivity.append({"campaign_id": row["campaign_id"],
                            "baseline_minus_20_net_value_usd": (row["baseline_hours"] * D("0.8") - row["actual_hours"]) * RATE - row["ai_cost_usd"],
                            "original_net_value_usd": row["net_ai_value_usd"],
                            "baseline_plus_20_net_value_usd": (row["baseline_hours"] * D("1.2") - row["actual_hours"]) * RATE - row["ai_cost_usd"]})
    write("sensitivity_summary.csv", sensitivity)
    print(f"Wrote 8 case-study evidence tables from {len(tasks)} unique tasks and {sum(t['prompt_count'] for t in tasks):,} prompts.")


if __name__ == "__main__":
    main()
