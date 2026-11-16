
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

## Additional Interface 
record_result(fixtures, fixture_id, home_score, away_score)
Engineer B — results.py
record_result(fixtures, fixture_id, home_score, away_score)

Validates the fixture and scores before mutation.

Rejects unknown fixture IDs.

Rejects fixtures already marked played.

Changes status to played only after successful validation.

Returns the updated fixture.

-

## Engineer B — Standings Contract

### Standings record

Each standings record must contain:

- `team_id`: string
- `team_name`: string
- `played`: integer
- `wins`: integer
- `draws`: integer
- `losses`: integer
- `goals_for`: integer
- `goals_against`: integer
- `goal_difference`: integer
- `points`: integer

Example:

{
    "team_id": "TM001",
    "team_name": "Red Comets",
    "played": 3,
    "wins": 2,
    "draws": 1,
    "losses": 0,
    "goals_for": 7,
    "goals_against": 3,
    "goal_difference": 4,
    "points": 7
}

### compute_standings(teams, fixtures)

- Returns a list of standings dictionaries.
- Includes every registered team, even those without played fixtures.
- Calculates statistics using only fixtures with status "played".
- Does not mutate teams or fixtures.
- Uses the agreed standings record structure.

### rank_standings(standings)

- Returns a new sorted list of standings dictionaries.
- Does not mutate the original standings.
- Sorts by:
  1. Points descending.
  2. Goal difference descending.
  3. Goals scored descending.
  4. Normalized team name ascending.

### Champion determination

A champion is unresolved when two or more leading teams have equal:

- Points.
- Goal difference.
- Goals scored.

Alphabetical display order must not be used to declare one of those teams the champion.

### Result recording integration

record_result(fixtures, fixture_id, home_score, away_score)

- Rejects unknown fixture IDs.
- Rejects fixtures already marked as played.
- Accepts nonnegative integers only.
- Explicitly rejects booleans, floats, strings and negative values.
- Validates all conditions before mutation.
- Returns the updated fixture.

### Shared mutation rules

- Team registration mutates the teams list only after validation.
- Result recording mutates fixtures only after successful validation.
- Standings calculation and ranking do not mutate their inputs.
- Persistence validates data before saving or returning loaded data.

}
