
def _get_team_ids(teams):
    """Validate the team records and return their IDs."""

    if not isinstance(teams, list):
        raise TypeError("Teams must be stored in a list.")

    if not 4 <= len(teams) <= 8:
        raise ValueError("A tournament requires between 4 and 8 teams.")

    team_ids = []

    for team in teams:
        if not isinstance(team, dict):
            raise ValueError("Every team must be a dictionary.")

        team_id = team.get("id")

        if not isinstance(team_id, str) or not team_id:
            raise ValueError("Every team must have a valid ID.")

        if team_id in team_ids:
            raise ValueError("Team IDs must be unique.")

        team_ids.append(team_id)

    return team_ids


def generate_fixtures(teams):
    """
    Generate a single round-robin fixture list.

    Every team plays every other team exactly once.
    The original teams list is not modified.
    """

    team_ids = _get_team_ids(teams)

    fixtures = []

    for i in range(len(team_ids)):
        for j in range(i + 1, len(team_ids)):

            fixture = {
                "id": f"M{len(fixtures) + 1:03d}",
                "home_id": team_ids[i],
                "away_id": team_ids[j],
                "status": "pending",
                "home_score": None,
                "away_score": None
            }

            fixtures.append(fixture)

    validate_fixtures(teams, fixtures)

    return fixtures


def validate_fixtures(teams, fixtures):
    """
    Validate fixture structure, references and schedule completeness.

    Returns True if valid.
    Raises TypeError or ValueError if invalid.
    """

    team_ids = _get_team_ids(teams)

    if not isinstance(fixtures, list):
        raise TypeError("Fixtures must be stored in a list.")

    expected_pairs = set()

    for i in range(len(team_ids)):
        for j in range(i + 1, len(team_ids)):
            expected_pairs.add(frozenset((team_ids[i], team_ids[j])))

    if len(fixtures) != len(expected_pairs):
        raise ValueError("Fixture count does not match the expected schedule.")

    fixture_ids = set()
    actual_pairs = set()

    required_fields = {
        "id",
        "home_id",
        "away_id",
        "status",
        "home_score",
        "away_score"
    }

    for fixture in fixtures:

        if not isinstance(fixture, dict):
            raise ValueError("Every fixture must be a dictionary.")

        if not required_fields.issubset(fixture):
            raise ValueError("A fixture is missing required fields.")

        fixture_id = fixture["id"]

        if not isinstance(fixture_id, str):
            raise ValueError("Fixture ID must be a string.")
        
        if (
            len(fixture_id) != 4
            or not fixture_id.startswith("M")
            or not fixture_id[1:].isdigit()
            or int(fixture_id[1:]) < 1
        ):
            raise ValueError("Fixture ID must follow the M001 format.")

        if fixture_id in fixture_ids:
            raise ValueError("Fixture IDs must be unique.")

        fixture_ids.add(fixture_id)

        home_id = fixture["home_id"]
        away_id = fixture["away_id"]

        if home_id not in team_ids or away_id not in team_ids:
            raise ValueError("Fixture references an unknown team.")

        if home_id == away_id:
            raise ValueError("A team cannot play against itself.")

        pair = frozenset((home_id, away_id))

        if pair in actual_pairs:
            raise ValueError("Duplicate team pairing detected.")

        actual_pairs.add(pair)

        status = fixture["status"]
        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        if status == "pending":
            if home_score is not None or away_score is not None:
                raise ValueError(
                    "Pending fixtures must not have scores."
                )

        elif status == "played":
            for score in (home_score, away_score):
                if type(score) is not int or score < 0:
                    raise ValueError(
                        "Played fixture scores must be nonnegative integers."
                    )

        else:
            raise ValueError("Fixture status must be pending or played.")

    if actual_pairs != expected_pairs:
        raise ValueError("The fixture list does not contain every team pairing.")

    return True
