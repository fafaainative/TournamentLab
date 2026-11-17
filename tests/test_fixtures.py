
import unittest

from tournament.fixtures import (
    generate_fixtures,
    validate_fixtures
)


class TestFixtureGeneration(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Hawks"},
            {"id": "TM003", "name": "Golden Eagles"},
            {"id": "TM004", "name": "Black Panthers"}
        ]

    def test_four_teams_generate_six_fixtures(self):
        fixtures = generate_fixtures(self.teams)

        self.assertEqual(len(fixtures), 6)

    def test_six_teams_generate_fifteen_fixtures(self):
        teams = [
            {"id": f"TM{i:03d}", "name": f"Team {i}"}
            for i in range(1, 7)
        ]

        fixtures = generate_fixtures(teams)

        self.assertEqual(len(fixtures), 15)

    def test_eight_teams_generate_twenty_eight_fixtures(self):
        teams = [
            {"id": f"TM{i:03d}", "name": f"Team {i}"}
            for i in range(1, 9)
        ]

        fixtures = generate_fixtures(teams)

        self.assertEqual(len(fixtures), 28)

    def test_fewer_than_four_teams_are_rejected(self):
        with self.assertRaises(ValueError):
            generate_fixtures(self.teams[:3])

    def test_more_than_eight_teams_are_rejected(self):
        teams = [
            {"id": f"TM{i:03d}", "name": f"Team {i}"}
            for i in range(1, 10)
        ]

        with self.assertRaises(ValueError):
            generate_fixtures(teams)

    def test_fixture_ids_are_unique(self):
        fixtures = generate_fixtures(self.teams)

        fixture_ids = [fixture["id"] for fixture in fixtures]

        self.assertEqual(len(fixture_ids), len(set(fixture_ids)))

    def test_fixture_ids_follow_expected_sequence(self):
        fixtures = generate_fixtures(self.teams)

        expected_ids = [
            "M001", "M002", "M003",
            "M004", "M005", "M006"
        ]

        self.assertEqual(
            [fixture["id"] for fixture in fixtures],
            expected_ids
        )

    def test_fixtures_have_no_self_match(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertNotEqual(
                fixture["home_id"],
                fixture["away_id"]
            )

    def test_each_unordered_pair_appears_once(self):
        fixtures = generate_fixtures(self.teams)

        pairs = [
            frozenset((fixture["home_id"], fixture["away_id"]))
            for fixture in fixtures
        ]

        self.assertEqual(len(pairs), len(set(pairs)))

    def test_each_team_plays_three_matches(self):
        fixtures = generate_fixtures(self.teams)

        for team in self.teams:
            appearances = sum(
                team["id"] in (fixture["home_id"], fixture["away_id"])
                for fixture in fixtures
            )

            self.assertEqual(appearances, 3)

    def test_fixtures_start_as_pending(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertEqual(fixture["status"], "pending")
            self.assertIsNone(fixture["home_score"])
            self.assertIsNone(fixture["away_score"])

    def test_generation_does_not_modify_teams(self):
        original_teams = [team.copy() for team in self.teams]

        generate_fixtures(self.teams)

        self.assertEqual(self.teams, original_teams)

    def test_duplicate_team_ids_are_rejected(self):
        teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM001", "name": "Blue Hawks"},
            {"id": "TM003", "name": "Golden Eagles"},
            {"id": "TM004", "name": "Black Panthers"}
        ]

        with self.assertRaises(ValueError):
            generate_fixtures(teams)

    def test_invalid_team_record_is_rejected(self):
        teams = [
            {"id": "TM001", "name": "Red Comets"},
            None,
            {"id": "TM003", "name": "Golden Eagles"},
            {"id": "TM004", "name": "Black Panthers"}
        ]

        with self.assertRaises(ValueError):
            generate_fixtures(teams)


class TestFixtureValidation(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Hawks"},
            {"id": "TM003", "name": "Golden Eagles"},
            {"id": "TM004", "name": "Black Panthers"}
        ]

        self.fixtures = generate_fixtures(self.teams)

    def test_valid_fixture_schedule_is_accepted(self):
        self.assertTrue(
            validate_fixtures(self.teams, self.fixtures)
        )

    def test_non_list_fixtures_are_rejected(self):
        with self.assertRaises(TypeError):
            validate_fixtures(self.teams, {})

    def test_duplicate_fixture_ids_are_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[1]["id"] = fixtures[0]["id"]

        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)

    def test_unknown_team_reference_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["home_id"] = "TM999"

        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)

    def test_reversed_duplicate_pairing_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]

        fixtures[1]["home_id"] = fixtures[0]["away_id"]
        fixtures[1]["away_id"] = fixtures[0]["home_id"]

        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)

    def test_missing_fixture_is_rejected(self):
        fixtures = self.fixtures[:-1]

        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)

    def test_invalid_status_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["status"] = "cancelled"

        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)

    def test_pending_fixture_cannot_have_scores(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["home_score"] = 2

        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)

    def test_played_fixture_accepts_valid_scores(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]

        fixtures[0]["status"] = "played"
        fixtures[0]["home_score"] = 2
        fixtures[0]["away_score"] = 1

        self.assertTrue(
            validate_fixtures(self.teams, fixtures)
        )

    def test_played_fixture_rejects_boolean_scores(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]

        fixtures[0]["status"] = "played"
        fixtures[0]["home_score"] = True
        fixtures[0]["away_score"] = 1

        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)

    def test_played_fixture_rejects_negative_scores(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]

        fixtures[0]["status"] = "played"
        fixtures[0]["home_score"] = -1
        fixtures[0]["away_score"] = 0

        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)
    def test_self_match_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["away_id"] = fixtures[0]["home_id"]
        
        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)


    def test_invalid_fixture_id_format_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["id"] = "M1"
        
        with self.assertRaises(ValueError):
            validate_fixtures(self.teams, fixtures)


if __name__ == "__main__":
    unittest.main()
