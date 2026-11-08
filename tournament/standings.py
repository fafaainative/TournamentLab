"""Calculate league standings from played fixtures."""


def _new_row(team):
    """Return a zeroed statistics row for one team."""
    return {
        "team_id": team["id"],
        "team_name": team["name"],
        "played": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0,
        "goal_difference": 0,
        "points": 0,
    }


def compute_standings(teams, fixtures):
    """Build the league table from played fixtures only."""
    # Every team starts with a zeroed row so unplayed teams still appear.
    table = {team["id"]: _new_row(team) for team in teams}

    for fixture in fixtures:
        # Only count matches that have actually been played.
        if fixture["status"] != "played":
            continue

        if fixture["home_id"] not in table or fixture["away_id"] not in table:
            raise ValueError(f"Fixture {fixture['id']} refers to an unknown team.")

        home = table[fixture["home_id"]]
        away = table[fixture["away_id"]]
        home_goals = fixture["home_score"]
        away_goals = fixture["away_score"]

        home["played"] += 1
        away["played"] += 1
        home["goals_for"] += home_goals
        home["goals_against"] += away_goals
        away["goals_for"] += away_goals
        away["goals_against"] += home_goals

        if home_goals > away_goals:
            home["wins"] += 1
            home["points"] += 3
            away["losses"] += 1
        elif away_goals > home_goals:
            away["wins"] += 1
            away["points"] += 3
            home["losses"] += 1
        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    # Goal difference is derived once all goals are totalled.
    for row in table.values():
        row["goal_difference"] = row["goals_for"] - row["goals_against"]

    return list(table.values())