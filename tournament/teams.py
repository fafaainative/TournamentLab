
def validate_team_name(name, teams):
    """
    Validate a proposed team name.

    Returns the trimmed team name if valid.
    Raises TypeError or ValueError if invalid.
    """

    if not isinstance(teams, list):
        raise TypeError("Teams must be stored in a list.")

    if not isinstance(name, str):
        raise TypeError("Team name must be a string.")

    cleaned_name = name.strip()

    if not 2 <= len(cleaned_name) <= 30:
        raise ValueError(
            "Team name must be between 2 and 30 characters."
        )

    for team in teams:
        existing_name = team.get("name")

        if isinstance(existing_name, str):
            if existing_name.strip().casefold() == cleaned_name.casefold():
                raise ValueError("A team with this name already exists.")

    return cleaned_name


def _generate_team_id(teams):
    """
    Generate the next sequential team ID.

    Uses the highest existing numeric suffix to avoid reusing IDs.
    """

    highest_id = 0

    for team in teams:
        team_id = team.get("id")

        if not isinstance(team_id, str) or not team_id.startswith("TM"):
            raise ValueError("An existing team has an invalid ID.")

        numeric_part = team_id[2:]

        if not numeric_part.isdigit() or int(numeric_part) < 1:
            raise ValueError("An existing team has an invalid ID.")

        highest_id = max(highest_id, int(numeric_part))

    return f"TM{highest_id + 1:03d}"


def register_team(teams, name):
    """
    Validate and register a team.

    Mutates the teams list only after all validation succeeds.
    Returns the newly registered team dictionary.
    """

    if not isinstance(teams, list):
        raise TypeError("Teams must be stored in a list.")

    cleaned_name = validate_team_name(name, teams)

    if len(teams) >= 8:
        raise ValueError("A tournament cannot have more than 8 teams.")

    team = {
        "id": _generate_team_id(teams),
        "name": cleaned_name
    }

    teams.append(team)

    return team


def list_teams(teams):
    """
    Return a copy of the registered teams.

    Changes to the returned dictionaries will not modify
    the original team records.
    """

    if not isinstance(teams, list):
        raise TypeError("Teams must be stored in a list.")

    return [team.copy() for team in teams]
