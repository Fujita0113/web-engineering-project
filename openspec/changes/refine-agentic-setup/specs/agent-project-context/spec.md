## ADDED Requirements

### Requirement: CLAUDE.md states a version-pinning policy for the stack

`CLAUDE.md` SHALL document the planned Django version and require the latest
stable version to be reconfirmed and pinned before the dependency is added, so
the agent does not select a version from memory.

#### Scenario: Django version guidance is present

- **WHEN** the agent reads `CLAUDE.md` before adding Django
- **THEN** it finds the current stable/LTS version reference and an instruction
  to reconfirm the latest version and pin it (no `latest`/`*`) at install time

### Requirement: CLAUDE.md documents layering conventions

`CLAUDE.md` SHALL describe where business logic, query logic, and view logic
belong so the agent places new Django code consistently.

#### Scenario: Layering rules are discoverable

- **WHEN** the agent plans new feature code
- **THEN** `CLAUDE.md` specifies that business logic goes in `services.py`,
  read/query logic in `selectors.py`, and that views stay thin

### Requirement: CLAUDE.md lists break risks and change coupling

`CLAUDE.md` SHALL maintain an "easy to break" checklist and a change-coupling
list so the agent checks related files when making risky edits.

#### Scenario: Break-risk checklist guides risky edits

- **WHEN** the agent modifies a model, a URL name, or auth logic
- **THEN** `CLAUDE.md` points it to the coupled artifacts to re-check
  (migrations, templates, `{% url %}` tags, login-required decorators)
