import unittest

from tournament.results import record_result


def make_fixtures():
    return [
        {"id": "M001", "home_id": "TM001", "away_id": "TM002",
         "status": "pending", "home_score": None, "away_score": None},
        {"id": "M002", "home_id": "TM003", "away_id": "TM004",
         "status": "pending", "home_score": None, "away_score": None},
    ]


class TestRecordResultValid(unittest.TestCase):
    def test_valid_home_win(self):
        fixtures = make_fixtures()
        fixture = record_result(fixtures, "M001", 3, 1)
        self.assertEqual(fixture["home_score"], 3)
        self.assertEqual(fixture["away_score"], 1)
        self.assertEqual(fixture["status"], "played")

    def test_valid_draw_with_zeros(self):
        fixtures = make_fixtures()
        fixture = record_result(fixtures, "M001", 0, 0)
        self.assertEqual(fixture["status"], "played")


class TestRecordResultRejections(unittest.TestCase):
    def test_boolean_score_rejected(self):
        fixtures = make_fixtures()
        with self.assertRaises(ValueError):
            record_result(fixtures, "M001", True, 1)

    def test_invalid_away_score_leaves_fixture_unchanged(self):
        fixtures = make_fixtures()
        with self.assertRaises(ValueError):
            record_result(fixtures, "M001", 2, -1)
        self.assertEqual(fixtures[0]["status"], "pending")
        self.assertIsNone(fixtures[0]["home_score"])
        self.assertIsNone(fixtures[0]["away_score"])

    def test_second_submission_rejected_and_original_kept(self):
        fixtures = make_fixtures()
        record_result(fixtures, "M001", 2, 1)
        with self.assertRaises(ValueError):
            record_result(fixtures, "M001", 9, 9)
        self.assertEqual(fixtures[0]["home_score"], 2)
        self.assertEqual(fixtures[0]["away_score"], 1)


if __name__ == "__main__":
    unittest.main()