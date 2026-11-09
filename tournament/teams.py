"""Team registration, validation, and lookup for TournamentLab."""


def _generate_team_id(teams):
    """Generate the next unique team ID."""

    numbers = []

    for team in teams:
        team_id = team["id"]

        if not team_id.startswith("TM") or not team_id[2:].isdigit():
            raise ValueError("Existing team ID has an invalid format.")

        numbers.append(int(team_id[2:]))

    next_number = max(numbers, default=0) + 1

    return f"TM{next_number:03d}"


def register_team(teams, name):
    """Validate and register a new team."""

    if not isinstance(name, str):
        raise ValueError("Team name must be a string.")

    name = name.strip()

    if not 2 <= len(name) <= 30:
        raise ValueError("Team name must contain 2–30 characters.")

    normalized_name = name.casefold()

    for team in teams:
        if team["name"].strip().casefold() == normalized_name:
            raise ValueError("A team with this name already exists.")

    team_id = _generate_team_id(teams)

    new_team = {
        "id": team_id,
        "name": name
    }

    teams.append(new_team)

    return new_team


def list_teams(teams):
    """Return a copy of the registered teams list."""

    return list(teams)


def find_team(teams, team_id):
    """Find a team using its unique ID."""

    for team in teams:
        if team["id"] == team_id:
            return team

    return None
    