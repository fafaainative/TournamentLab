import unittest

from tournament.teams import (
    register_team,
    list_teams,
    find_team,
)


class TestTeamRegistration(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Strikers"},
        ]

    def test_register_valid_team(self):
        team = register_team(self.teams, "Green Eagles")

        self.assertEqual(team["id"], "TM003")
        self.assertEqual(team["name"], "Green Eagles")
        self.assertEqual(len(self.teams), 3)

    def test_name_whitespace_is_removed(self):
        team = register_team(self.teams, "  Green Eagles  ")

        self.assertEqual(team["name"], "Green Eagles")

    def test_duplicate_name_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "Red Comets")

    def test_case_insensitive_duplicate_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "RED COMETS")

    def test_short_name_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "A")

    def test_long_name_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "A" * 31)

    def test_non_string_name_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, 123)

    def test_id_generation_handles_gaps(self):
        teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM004", "name": "Blue Strikers"},
        ]

        team = register_team(teams, "Green Eagles")

        self.assertEqual(team["id"], "TM005")

    def test_empty_list_starts_with_tm001(self):
        teams = []

        team = register_team(teams, "Red Comets")

        self.assertEqual(team["id"], "TM001")

    def test_failed_registration_does_not_mutate_list(self):
        original_teams = list(self.teams)

        with self.assertRaises(ValueError):
            register_team(self.teams, "Red Comets")

        self.assertEqual(self.teams, original_teams)

    def test_list_teams_returns_separate_list(self):
        result = list_teams(self.teams)

        self.assertEqual(result, self.teams)
        self.assertIsNot(result, self.teams)

    def test_find_existing_team(self):
        result = find_team(self.teams, "TM001")

        self.assertEqual(result["name"], "Red Comets")

    def test_find_missing_team(self):
        result = find_team(self.teams, "TM999")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
