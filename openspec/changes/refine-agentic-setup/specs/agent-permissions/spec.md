## ADDED Requirements

### Requirement: Committed project permission policy

The project SHALL provide a committed `.claude/settings.json` that defines the
agent's permission policy so that the same allow/deny behavior applies for every
collaborator and session.

#### Scenario: Settings file is present and valid

- **WHEN** the repository is checked out
- **THEN** `.claude/settings.json` exists at the repo root and parses as valid
  JSON with a `permissions.allow` array

### Requirement: Safe dev commands run without a prompt

The permission policy SHALL allowlist repeatable, non-destructive development
commands so the agent can run them without interrupting the user for
confirmation.

#### Scenario: Test, lint, and Django management commands are allowed

- **WHEN** the agent runs `uv run pytest`, `uv run ruff`, or
  `uv run python manage.py <subcommand>`
- **THEN** the command executes without a permission prompt

#### Scenario: Read-only and additive git commands are allowed

- **WHEN** the agent runs `git status`, `git diff`, `git log`, `git show`,
  `git branch`, or `git add`
- **THEN** the command executes without a permission prompt

### Requirement: Irreversible operations always require confirmation

The permission policy SHALL NOT allowlist commands that are hard to reverse, so
that the user is always prompted before they run.

#### Scenario: Destructive git and filesystem operations are not pre-approved

- **WHEN** the agent attempts `git commit`, `git push`, `git reset`, or a file
  deletion
- **THEN** the command is not in the allowlist and the user is prompted for
  confirmation
