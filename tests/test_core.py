import unittest

from src.mymis import (
    check_guardrails,
    compare_binary,
    experiment_decision,
    minimum_detectable_lift,
    sample_ratio_mismatch,
    summarize_funnel,
    validate_events,
    weekly_retention,
)


class CoreTests(unittest.TestCase):
    def test_experiment_includes_confidence_interval(self):
        result = compare_binary(100, 1000, 130, 1000)
        self.assertGreater(result["absolute_lift"], 0)
        self.assertLess(result["p_value"], 0.1)
        low, high = result["absolute_lift_ci"]
        self.assertLess(low, result["absolute_lift"])
        self.assertGreater(high, result["absolute_lift"])

    def test_srm(self):
        self.assertFalse(sample_ratio_mismatch(5000, 5000)["flag"])
        self.assertTrue(sample_ratio_mismatch(7000, 3000)["flag"])

    def test_mde_shrinks_with_larger_sample(self):
        self.assertGreater(
            minimum_detectable_lift(0.1, 1000),
            minimum_detectable_lift(0.1, 10000),
        )

    def test_funnel(self):
        result = summarize_funnel([("visit", 100), ("signup", 50)])
        self.assertEqual(result[1]["from_previous"], 0.5)

    def test_contract(self):
        rows = [
            {"event_id": "x", "user_id": "u", "event_name": "a", "timestamp": "t"},
            {"event_id": "x", "user_id": "u", "event_name": "b", "timestamp": "t"},
        ]
        self.assertEqual(len(validate_events(rows)), 1)

    def test_weekly_retention_deduplicates_users(self):
        events = [
            {"user_id": "u1", "event_name": "signup", "timestamp": "2026-09-30T10:00:00+08:00"},
            {"user_id": "u1", "event_name": "open", "timestamp": "2026-10-07T10:00:00+08:00"},
            {"user_id": "u1", "event_name": "open", "timestamp": "2026-10-08T10:00:00+08:00"},
            {"user_id": "u2", "event_name": "signup", "timestamp": "2026-10-01T10:00:00+08:00"},
            {"user_id": "u2", "event_name": "open", "timestamp": "2026-10-16T10:00:00+08:00"},
        ]
        rows = weekly_retention(
            events,
            activity_events={"open"},
            max_week=2,
            reporting_timezone="Asia/Taipei",
        )
        by_week = {row["week"]: row for row in rows}
        self.assertEqual(by_week[0]["cohort_size"], 2)
        self.assertEqual(by_week[1]["users"], 1)
        self.assertEqual(by_week[2]["users"], 1)

    def test_guardrail_and_decision(self):
        primary = compare_binary(1000, 10000, 1120, 10000)
        srm = sample_ratio_mismatch(10000, 10000)
        guardrails = check_guardrails([
            {
                "name": "crash_free",
                "control": 0.995,
                "variant": 0.994,
                "mode": "min",
                "tolerance": 0.002,
            },
        ])
        self.assertEqual(
            experiment_decision(primary, srm, guardrails)["decision"],
            "ship",
        )

    def test_guardrail_breach_holds_experiment(self):
        primary = compare_binary(1000, 10000, 1120, 10000)
        srm = sample_ratio_mismatch(10000, 10000)
        guardrails = check_guardrails([
            {
                "name": "crash_free",
                "control": 0.995,
                "variant": 0.98,
                "mode": "min",
                "tolerance": 0.002,
            },
        ])
        self.assertEqual(
            experiment_decision(primary, srm, guardrails)["decision"],
            "hold",
        )


if __name__ == "__main__":
    unittest.main()
