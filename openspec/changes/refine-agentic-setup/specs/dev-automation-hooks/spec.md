## ADDED Requirements

### Requirement: Opt-in lint/format automation hook

The project SHALL offer an opt-in Claude Code hook that runs `ruff format` and
`ruff check` so formatting and lint stay consistent without manual steps. The
hook MUST be opt-in and MUST NOT block normal editing when disabled.

#### Scenario: Hook formats and lints after edits when enabled

- **WHEN** the hook is configured and the agent finishes a batch of file edits
- **THEN** `ruff format` and `ruff check` run against the project and any
  remaining lint findings are surfaced to the user

#### Scenario: Project works normally without the hook

- **WHEN** the hook is not configured
- **THEN** editing, testing, and committing proceed normally with no errors from
  a missing hook

### Requirement: Hook does not perform destructive or unattended actions

The automation hook SHALL be limited to formatting and lint reporting and MUST
NOT commit, push, or delete files automatically.

#### Scenario: Hook stays within safe operations

- **WHEN** the automation hook runs
- **THEN** it only formats and reports lint results, and does not run any git
  write or file-deletion command
