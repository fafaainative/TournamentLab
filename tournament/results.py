"""Record match results safely for TournamentLab."""


def is_valid_score(value):
    """Return True only for a genuine nonnegative int (not a bool)."""

    #True and False count as integers in Python, so remove them by hand
    if isinstance(value, bool):
        return False
    if not isinstance(value, int):
        return False
    return value >= 0


def _find_fixture(fixtures, fixture_id):
    """Return the fixture with the given ID, or None if it does not exist."""
    for fixture in fixtures:
        if fixture["id"] == fixture_id:
            return fixture
    return None


def record_result(fixtures, fixture_id, home_score, away_score):
    """Record a score for a pending fixture and return the updated fixture."""
    fixture = _find_fixture(fixtures, fixture_id)
    if fixture is None:
        raise ValueError(f"Unknown fixture ID: {fixture_id}")

    if fixture["status"] != "pending":
        raise ValueError(f"Fixture {fixture_id} has already been played.")

    
    #check that both scores are valid before mutation
    if not is_valid_score(home_score):
        raise ValueError(f"Invalid home score: {home_score!r}")
    if not is_valid_score(away_score):
        raise ValueError(f"Invalid away score: {away_score!r}")

    #Only reached when every check has passed.
    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["status"] = "played"
    return fixture