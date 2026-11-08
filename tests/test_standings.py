import copy
import unittest

from tournament.standings import compute_standings


def make_teams():
    return [
        {"id": "TM001", "name": "Red Comets"},
        {"id": "TM002", "name": "Blue Wolves"},
        {"id": "TM003", "name": "Green Hawks"},
    ]


def make_fixture(fid, home, away, status="pending", hs=None, as_=None):
    return {"id": fid, "home_id": home, "away_id": away,
            "status": status, "home_score": hs, "away_score": as_}


def row_for(table, team_id):
    return next(r for r in table if r["team_id"] == team_id)


class TestComputeStandings(unittest.TestCase):
    def test_win_awards_three_points_and_loss_zero(self):
        fixtures = [make_fixture("M001", "TM001", "TM002", "played", 3, 1)]
        table = compute_standings(make_teams(), fixtures)
        self.assertEqual(row_for(table, "TM001")["points"], 3)
        self.assertEqual(row_for(table, "TM002")["points"], 0)
        self.assertEqual(row_for(table, "TM001")["goal_difference"], 2)
        self.assertEqual(row_for(table, "TM002")["goal_difference"], -2)

    def test_draw_awards_one_point_each(self):
        fixtures = [make_fixture("M001", "TM001", "TM002", "played", 2, 2)]
        table = compute_standings(make_teams(), fixtures)
        self.assertEqual(row_for(table, "TM001")["points"], 1)
        self.assertEqual(row_for(table, "TM002")["points"], 1)

    def test_pending_ignored_and_unplayed_team_appears(self):
        fixtures = [make_fixture("M001", "TM001", "TM002")]
        table = compute_standings(make_teams(), fixtures)
        self.assertEqual(len(table), 3)
        self.assertEqual(row_for(table, "TM003")["played"], 0)
        self.assertEqual(row_for(table, "TM001")["points"], 0)

    def test_inputs_are_not_modified(self):
        teams, fixtures = make_teams(), [make_fixture("M001", "TM001", "TM002", "played", 1, 0)]
        teams_before, fixtures_before = copy.deepcopy(teams), copy.deepcopy(fixtures)
        compute_standings(teams, fixtures)
        self.assertEqual(teams, teams_before)
        self.assertEqual(fixtures, fixtures_before)


if __name__ == "__main__":
    unittest.main()