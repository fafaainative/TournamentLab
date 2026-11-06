Engineer A — Learning Log

Project: TournamentLab

Engineer: A
Branch: feat/1-team-scheduling

1. Progress Completed

Initialized the TournamentLab repository.

Created the project directories.

Initialized the tournament package.

Committed tournament/__init__.py.

Created tournament/teams.py for team registration and validation.

2. Concepts Studied

Lists containing dictionaries.

Function parameters and return values.

String normalization using .strip() and .casefold().

Validation before mutation.

Extracting numeric portions of team IDs using slicing.

Converting strings to integers using int().

Finding the highest existing team ID using max().

3. Engineering Decisions

Team IDs should be generated using the highest existing numeric ID rather than the number of records.

This prevents duplicate IDs when gaps exist in the sequence.

Example:

Existing IDs: TM001, TM002, TM004

Next ID: TM005

4. Current Challenges

Understanding string slicing in team ID extraction.

Handling an empty team list during ID generation.

Implementing safe ID generation.

5. Next Objectives

Complete the ID-generation helper.

Implement team registration and validation.

Write unit tests using unittest.

Review and commit the completed team module.

