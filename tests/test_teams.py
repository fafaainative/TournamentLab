
import unittest

from tournament.teams import (
    validate_team_name,
    register_team,
    list_teams,
    _generate_team_id
)


class TestTeamNameValidation(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Hawks"}
        ]

    def test_team_name_is_trimmed(self):
        result = validate_team_name("  Green Lions  ", self.teams)

        self.assertEqual(result, "Green Lions")

    def test_non_string_team_name_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_team_name(123, self.teams)

    def test_non_list_teams_container_is_rejected(self):
        with self.assertRaises(TypeError):
            validate_team_name("Green Lions", "not a list")

    def test_empty_team_name_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_team_name("", self.teams)

    def test_whitespace_only_team_name_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_team_name("     ", self.teams)

    def test_team_name_below_minimum_length_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_team_name("A", self.teams)

    def test_team_name_above_maximum_length_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_team_name("A" * 31, self.teams)

    def test_team_name_at_minimum_length_is_accepted(self):
        result = validate_team_name("AB", self.teams)

        self.assertEqual(result, "AB")

    def test_team_name_at_maximum_length_is_accepted(self):
        name = "A" * 30

        result = validate_team_name(name, self.teams)

        self.assertEqual(result, name)

    def test_duplicate_name_is_rejected_case_insensitively(self):
        with self.assertRaises(ValueError):
            validate_team_name("red comets", self.teams)

    def test_duplicate_name_with_extra_spaces_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_team_name("  RED COMETS  ", self.teams)

    def test_invalid_existing_team_record_is_rejected(self):
        teams = ["not a dictionary"]

        with self.assertRaises(ValueError):
            validate_team_name("Green Lions", teams)


class TestTeamRegistration(unittest.TestCase):

    def setUp(self):
        self.teams = []

    def test_team_is_registered_with_correct_structure(self):
        team = register_team(self.teams, "Red Comets")

        self.assertEqual(
            team,
            {
                "id": "TM001",
                "name": "Red Comets"
            }
        )

    def test_registered_team_is_added_to_teams_list(self):
        team = register_team(self.teams, "Red Comets")

        self.assertIn(team, self.teams)

    def test_team_name_is_trimmed_during_registration(self):
        team = register_team(self.teams, "  Blue Hawks  ")

        self.assertEqual(team["name"], "Blue Hawks")

    def test_team_ids_are_generated_sequentially(self):
        register_team(self.teams, "Red Comets")
        register_team(self.teams, "Blue Hawks")
        team = register_team(self.teams, "Green Lions")

        self.assertEqual(team["id"], "TM003")

    def test_next_id_uses_highest_existing_numeric_id(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM005", "name": "Blue Hawks"}
        ]

        team = register_team(self.teams, "Green Lions")

        self.assertEqual(team["id"], "TM006")

    def test_non_canonical_existing_team_id_is_rejected(self):
        invalid_ids = ["TM1", "TM01", "TM0001", "TM000"]

        for invalid_id in invalid_ids:
            with self.subTest(team_id=invalid_id):
                teams = [
                    {"id": invalid_id, "name": "Existing Team"}
                ]

                with self.assertRaises(ValueError):
                    register_team(teams, "New Team")

    def test_duplicate_existing_team_ids_are_rejected(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM001", "name": "Blue Hawks"}
        ]

        with self.assertRaises(ValueError):
            register_team(self.teams, "Green Lions")

    def test_team_id_generation_stops_at_tm999(self):
        teams = [
            {"id": "TM999", "name": "Last Team"}
        ]

        with self.assertRaises(ValueError):
            _generate_team_id(teams)

    def test_maximum_of_eight_teams_is_enforced(self):
        for number in range(8):
            register_team(self.teams, f"Team {number + 1}")

        with self.assertRaises(ValueError):
            register_team(self.teams, "Ninth Team")

        self.assertEqual(len(self.teams), 8)

    def test_invalid_registration_does_not_modify_teams(self):
        register_team(self.teams, "Red Comets")

        original_teams = [team.copy() for team in self.teams]

        with self.assertRaises(ValueError):
            register_team(self.teams, "red comets")

        self.assertEqual(self.teams, original_teams)

    def test_invalid_container_type_is_rejected(self):
        with self.assertRaises(TypeError):
            register_team("not a list", "Red Comets")

    def test_invalid_name_does_not_modify_teams(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, 123)

        self.assertEqual(self.teams, [])


class TestTeamListing(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Hawks"}
        ]

    def test_list_teams_returns_all_teams(self):
        result = list_teams(self.teams)

        self.assertEqual(result, self.teams)

    def test_list_teams_returns_a_new_list(self):
        result = list_teams(self.teams)

        self.assertIsNot(result, self.teams)

    def test_list_teams_returns_independent_dictionaries(self):
        result = list_teams(self.teams)

        self.assertIsNot(result[0], self.teams[0])

    def test_modifying_returned_list_does_not_modify_original(self):
        result = list_teams(self.teams)

        result.append({"id": "TM003", "name": "Green Lions"})

        self.assertEqual(len(self.teams), 2)

    def test_modifying_returned_team_does_not_modify_original(self):
        result = list_teams(self.teams)

        result[0]["name"] = "Changed Name"

        self.assertEqual(self.teams[0]["name"], "Red Comets")

    def test_non_list_container_is_rejected(self):
        with self.assertRaises(TypeError):
            list_teams("not a list")


if __name__ == "__main__":
    unittest.main()
