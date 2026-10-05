import unittest
from src.mymis import compare_binary, sample_ratio_mismatch, summarize_funnel, validate_events

class CoreTests(unittest.TestCase):
    def test_experiment(self):
        result = compare_binary(100, 1000, 130, 1000)
        self.assertGreater(result["absolute_lift"], 0)
        self.assertLess(result["p_value"], 0.1)

    def test_srm(self):
        self.assertFalse(sample_ratio_mismatch(5000, 5000)["flag"])
        self.assertTrue(sample_ratio_mismatch(7000, 3000)["flag"])

    def test_funnel(self):
        result = summarize_funnel([("a", 100), ("b", 50)])
        self.assertEqual(result[1]["from_previous"], 0.5)

    def test_contract(self):
        rows = [
            {"event_id":"x","user_id":"u","event_name":"a","timestamp":"t"},
            {"event_id":"x","user_id":"u","event_name":"b","timestamp":"t"},
        ]
        self.assertEqual(len(validate_events(rows)), 1)

if __name__ == "__main__":
    unittest.main()
