
import unittest

from tournament.teams import (
    validate_team_name,
    register_team,
    list_teams
)


class TestTeamRegistration(unittest.TestCase):

    def setUp(self):
        self.teams = []

    def test_valid_name_is_trimmed(self):
        result = validate_team_name("  Red Comets  ", self.teams)

        self.assertEqual(result, "Red Comets")

    def test_name_must_be_a_string(self):
        with self.assertRaises(TypeError):
            validate_team_name(123, self.teams)

    def test_teams_must_be_a_list(self):
        with self.assertRaises(TypeError):
            validate_team_name("Red Comets", {})

    def test_name_must_have_at_least_two_characters(self):
        with self.assertRaises(ValueError):
            validate_team_name("A", self.teams)

    def test_name_must_not_exceed_thirty_characters(self):
        with self.assertRaises(ValueError):
            validate_team_name("A" * 31, self.teams)

    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_team_name("   ", self.teams)

    def test_duplicate_name_is_rejected_case_insensitively(self):
        register_team(self.teams, "Red Comets")

        with self.assertRaises(ValueError):
            register_team(self.teams, "RED COMETS")

    def test_name_with_different_outer_whitespace_is_duplicate(self):
        register_team(self.teams, "Red Comets")

        with self.assertRaises(ValueError):
            register_team(self.teams, "  Red Comets  ")

    def test_team_is_registered_with_correct_structure(self):
        team = register_team(self.teams, "Red Comets")

        self.assertEqual(
            team,
            {
                "id": "TM001",
                "name": "Red Comets"
            }
        )

    def test_team_ids_increment(self):
        first = register_team(self.teams, "Red Comets")
        second = register_team(self.teams, "Blue Hawks")

        self.assertEqual(first["id"], "TM001")
        self.assertEqual(second["id"], "TM002")

    def test_id_uses_highest_existing_number(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM003", "name": "Blue Hawks"}
        ]

        team = register_team(self.teams, "Golden Eagles")

        self.assertEqual(team["id"], "TM004")

    def test_invalid_existing_id_is_rejected(self):
        self.teams = [
            {"id": "INVALID", "name": "Red Comets"}
        ]

        with self.assertRaises(ValueError):
            register_team(self.teams, "Blue Hawks")

    def test_maximum_of_eight_teams(self):
        for number in range(8):
            register_team(self.teams, f"Team {number + 1}")

        with self.assertRaises(ValueError):
            register_team(self.teams, "Ninth Team")

        self.assertEqual(len(self.teams), 8)

    def test_failed_registration_does_not_change_teams(self):
        register_team(self.teams, "Red Comets")

        original_teams = [team.copy() for team in self.teams]

        with self.assertRaises(ValueError):
            register_team(self.teams, "RED COMETS")

        self.assertEqual(self.teams, original_teams)

    def test_list_teams_returns_same_records(self):
        register_team(self.teams, "Red Comets")

        result = list_teams(self.teams)

        self.assertEqual(result, self.teams)

    def test_list_teams_returns_independent_copies(self):
        register_team(self.teams, "Red Comets")

        result = list_teams(self.teams)
        result[0]["name"] = "Changed Name"

        self.assertEqual(
            self.teams[0]["name"],
            "Red Comets"
        )

    def test_list_teams_rejects_invalid_container(self):
        with self.assertRaises(TypeError):
            list_teams({})


if __name__ == "__main__":
    unittest.main()
