
def validate_team_name(name, teams):
    """
    Validate and normalize a proposed team name.

    Returns the cleaned team name.
    Raises TypeError for an invalid teams container.
    Raises ValueError for invalid team-name data.
    """

    if not isinstance(teams, list):
        raise TypeError("Teams must be stored in a list.")

    if not isinstance(name, str):
        raise ValueError("Team name must be a string.")

    cleaned_name = name.strip()

    if not 2 <= len(cleaned_name) <= 30:
        raise ValueError(
            "Team name must be between 2 and 30 characters."
        )

    for team in teams:
        if not isinstance(team, dict):
            raise ValueError("Every existing team must be a dictionary.")

        existing_name = team.get("name")

        if isinstance(existing_name, str):
            if existing_name.strip().casefold() == cleaned_name.casefold():
                raise ValueError("A team with this name already exists.")

    return cleaned_name


def _generate_team_id(teams):
    """
    Generate the next available canonical team ID.

    IDs follow the format TM001, TM002, etc.
    Existing IDs must be valid and unique.
    """

    highest_id = 0
    existing_ids = set()

    for team in teams:
        if not isinstance(team, dict):
            raise ValueError("Every existing team must be a dictionary.")

        team_id = team.get("id")

        if (
            not isinstance(team_id, str)
            or len(team_id) != 5
            or not team_id.startswith("TM")
            or not team_id[2:].isdigit()
            or int(team_id[2:]) < 1
        ):
            raise ValueError("An existing team has an invalid ID.")

        if team_id in existing_ids:
            raise ValueError("Duplicate team IDs are not allowed.")

        existing_ids.add(team_id)

        numeric_part = int(team_id[2:])
        highest_id = max(highest_id, numeric_part)

    if highest_id >= 999:
        raise ValueError("No more team IDs are available.")

    return f"TM{highest_id + 1:03d}"


def register_team(teams, name):
    """
    Register a new tournament team.

    A tournament supports a maximum of eight registered teams.
    Team registration validates all data before modifying the list.

    Returns the newly created team dictionary.
    """

    if not isinstance(teams, list):
        raise TypeError("Teams must be stored in a list.")

    cleaned_name = validate_team_name(name, teams)

    if len(teams) >= 8:
        raise ValueError("A tournament cannot have more than 8 teams.")

    team_id = _generate_team_id(teams)

    team = {
        "id": team_id,
        "name": cleaned_name
    }

    teams.append(team)

    return team


def list_teams(teams):
    """
    Return a copy of the registered teams.

    The returned list and its team dictionaries are independent
    of the original list.
    """

    if not isinstance(teams, list):
        raise TypeError("Teams must be stored in a list.")

    return [team.copy() for team in teams]
