import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  prepare,
  summarize,
  selectTasks,
  wholeCampaigns,
  dailyUsage,
  uniqueBy,
  ratio,
} from "../dashboard/metrics.mjs";
const data = JSON.parse(
  readFileSync(new URL("../dashboard/demo-data.json", import.meta.url), "utf8"),
);
const model = prepare(data);
test("focal campaign values are computed from token rates and task hours", () => {
  const c1 = summarize(selectTasks(model.tasks, { campaign_id: "C001" }));
  const c2 = summarize(selectTasks(model.tasks, { campaign_id: "C002" }));
  assert.deepEqual(
    [c1.tasks, c1.cost, c1.baseline, c1.actual, c1.saved, c1.value, c1.roi],
    [60, 500, 240, 140, 100, 4500, 900],
  );
  assert.deepEqual(
    [c2.tasks, c2.cost, c2.baseline, c2.actual, c2.saved, c2.value, c2.roi],
    [60, 1400, 200, 270, -70, -4900, -350],
  );
});
test("aggregation does not multiply task hours or average task ratios", () => {
  const s = summarize(model.tasks);
  assert.equal(s.tasks, 240);
  assert.equal(
    s.actual,
    model.tasks.reduce((v, t) => v + Math.round(t.actual_hours * 100), 0) / 100,
  );
  assert.equal(s.roi, (s.value * 100) / s.cost);
  assert.equal(s.prompts, model.usage.length);
});
test("campaign profit stays whole while task cohort narrows", () => {
  const before = wholeCampaigns(model, "C002");
  const subset = selectTasks(model.tasks, {
    campaign_id: "C002",
    model: "Lite",
    department: "Content",
  });
  assert.ok(subset.length < 60);
  dailyUsage(model, subset, "2026-09-01", "2026-09-04");
  assert.deepEqual(wholeCampaigns(model, "C002"), before);
  assert.equal(before[0].result, -2400);
});
test("baseline sensitivity preserves focal conclusions at both endpoints", () => {
  for (const change of [-20, 20]) {
    assert.ok(
      summarize(selectTasks(model.tasks, { campaign_id: "C001" }), change)
        .value > 0,
    );
    assert.ok(
      summarize(selectTasks(model.tasks, { campaign_id: "C002" }), change)
        .value < 0,
    );
  }
});
test("daily cost reconciles to all prompts without rounding each charge to cents", () => {
  const daily = dailyUsage(model, model.tasks);
  assert.equal(
    daily.reduce((s, r) => s + r.inputMicro + r.outputMicro, 0),
    summarize(model.tasks).cost * 1e6,
  );
  const range = dailyUsage(model, model.tasks, "2026-09-10", "2026-09-15");
  assert.ok(
    range.every((r) => r.date >= "2026-09-10" && r.date <= "2026-09-15"),
  );
});
test("empty cohort and zero denominators show N/A ratios", () => {
  const empty = summarize(selectTasks(model.tasks, { campaign_id: "MISSING" }));
  assert.equal(empty.tasks, 0);
  assert.equal(empty.cost, 0);
  assert.equal(empty.roi, null);
  assert.equal(empty.costPerPrompt, null);
  assert.equal(ratio(10, 0), null);
});
test("duplicate IDs cannot silently create conflicting records", () => {
  assert.equal(
    uniqueBy(
      [
        { id: 1, value: 2 },
        { id: 1, value: 2 },
      ],
      "id",
    ).length,
    1,
  );
  assert.throws(
    () =>
      uniqueBy(
        [
          { id: 1, value: 2 },
          { id: 1, value: 3 },
        ],
        "id",
      ),
    /Conflicting/,
  );
});
test("all model and department combinations conserve their parent totals", () => {
  for (const key of ["department", "product", "model"]) {
    const parts = [...new Set(model.tasks.map((t) => t[key]))].map((value) =>
      summarize(selectTasks(model.tasks, { [key]: value })),
    );
    const all = summarize(model.tasks);
    assert.equal(
      parts.reduce((s, r) => s + r.prompts, 0),
      all.prompts,
    );
    assert.equal(
      parts.reduce((s, r) => s + Math.round(r.cost * 1e6), 0),
      Math.round(all.cost * 1e6),
    );
    assert.equal(
      parts.reduce((s, r) => s + Math.round(r.actual * 100), 0),
      Math.round(all.actual * 100),
    );
  }
});
