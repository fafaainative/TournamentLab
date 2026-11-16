
# TournamentLab Function Contracts

## 1. Team Management

### validate_team_name(name, teams)
Input:
- name: string
- teams: list of team dictionaries

Returns:
- Normalized team name.

Raises:
- ValueError for invalid or duplicate names.

### register_team(teams, name)
Input:
- teams: existing team list
- name: proposed team name

Returns:
- Newly registered team dictionary.

Mutation:
- Appends the new team to teams.

ID:
- TM001, TM002, etc.

### list_teams(teams)
Returns:
- Registered teams without modifying the input.

## 2. Fixture Management

### generate_fixtures(teams)
Returns:
- A new list of fixture dictionaries.

Rules:
- Four to eight teams.
- Every unordered pair exactly once.
- IDs M001, M002, etc.
- Initial status pending.

### validate_fixtures(teams, fixtures)
Returns:
- True when fixture integrity is valid.

Raises:
- ValueError for invalid references,
  duplicate IDs, self-fixtures or duplicate pairs.

## 3. Persistence

### save_tournament(path, teams, fixtures)
- Saves schema_version 1.
- Validates before writing.
- Preserves the previous file if validation fails.

### load_tournament(path)
- Reads JSON.
- Validates the complete document.
- Returns validated tournament data.
- Does not modify active application state.

### validate_tournament_data(data)
- Validates schema version.
- Validates teams and fixtures.
- Validates IDs and references.
- Validates fixture status and scores.

## 4. Canonical Data Structures

Team:
{
    "id": "TM001",
    "name": "Red Comets"
}

Fixture:
{
    "id": "M001",
    "home_id": "TM001",
    "away_id": "TM002",
    "status": "pending",
    "home_score": null,
    "away_score": null
}

## 5. Shared Data Rules

Fixture statuses:
- pending
- played

Pending fixtures must have null scores.

Played fixtures must have nonnegative integer scores.
Boolean values are not valid scores.

## 6. Error Handling

Use ValueError for invalid business data.

Use appropriate file and JSON exceptions for
file access and malformed JSON.

## 7. Change Management

Both engineers must agree before changing
shared function signatures or data structures.
