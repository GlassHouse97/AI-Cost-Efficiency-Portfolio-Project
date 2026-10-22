"""Regression checks for the analytical failure modes, using Python stdlib."""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_data", ROOT / "scripts/validate_data.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class SourceIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = validator.load(ROOT)

    def test_reconciles_both_tracks_and_exact_targets(self):
        result = validator.validate_data(copy.deepcopy(self.source))
        self.assertEqual(result["clean_tasks"], 240)
        self.assertEqual(result["campaigns"]["C001"]["actual_hours"], 140)
        self.assertEqual(result["campaigns"]["C002"]["campaign_result_usd"], -2400)

    def test_conflicting_duplicate_is_rejected(self):
        data = copy.deepcopy(self.source)
        data["work_log"][-1]["actual_hours"] = "999"
        with self.assertRaisesRegex(ValueError, "Conflicting duplicate"):
            validator.validate_data(data)

    def test_unknown_price_is_rejected(self):
        data = copy.deepcopy(self.source)
        data["ai_usage"][0]["model"] = "Missing"
        with self.assertRaisesRegex(ValueError, "model foreign key"):
            validator.validate_data(data)

    def test_noninteger_tokens_are_rejected(self):
        data = copy.deepcopy(self.source)
        data["ai_usage"][0]["input_tokens"] = "12.5"
        with self.assertRaisesRegex(ValueError, "nonnegative integers"):
            validator.validate_data(data)

    def test_mismatched_campaign_join_is_rejected(self):
        data = copy.deepcopy(self.source)
        data["ai_usage"][0]["campaign_id"] = "C004"
        with self.assertRaisesRegex(ValueError, "campaign agreement"):
            validator.validate_data(data)

    def test_rework_cannot_be_added_outside_actual_time(self):
        data = copy.deepcopy(self.source)
        data["work_log"][0]["rework_hours"] = "1000"
        with self.assertRaisesRegex(ValueError, "Rework is inside"):
            validator.validate_data(data)

    def test_wrong_quick_rate_is_rejected(self):
        data = copy.deepcopy(self.source)
        data["quick"][0]["input_rate_usd_per_million"] = "99"
        with self.assertRaisesRegex(ValueError, "Quick prices"):
            validator.validate_data(data)

    def test_demo_must_match_source(self):
        data = copy.deepcopy(self.source)
        data["demo"]["work_log"][0]["actual_hours"] += 0.01
        with self.assertRaisesRegex(ValueError, "Demo numeric"):
            validator.validate_data(data)

    def test_repeated_prompts_cannot_silently_multiply_tasks(self):
        data = copy.deepcopy(self.source)
        data["ai_usage"].append(dict(data["ai_usage"][0]))
        with self.assertRaisesRegex(ValueError, "Usage IDs unique"):
            validator.validate_data(data)

    def test_cost_is_not_rounded_per_prompt(self):
        result = validator.validate_data(copy.deepcopy(self.source))
        self.assertEqual(result["campaigns"]["C001"]["ai_cost_usd"], validator.D("500.000000"))
        self.assertEqual(result["campaigns"]["C002"]["ai_cost_usd"], validator.D("1400.000000"))


if __name__ == "__main__":
    unittest.main()
