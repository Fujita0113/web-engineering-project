## Why

The repository has rich project context (`CLAUDE.md`, OpenSpec) but lacks an
explicit, version-controlled agent operating configuration: there is no
`.claude/settings.json`, so every safe dev command (`uv run pytest`, `ruff`,
`python manage.py`) triggers a permission prompt, and no automation enforces the
lint/format and version-pinning conventions the project already documents. As
the project grows from skeleton into a Django app, a deliberate agentic setup
keeps the agent fast, safe, and consistent.

## What Changes

- Introduce a committed project permission policy (`.claude/settings.json`) that
  allowlists safe, repeatable dev commands and intentionally leaves irreversible
  operations (`git commit`/`push`/`reset`, file deletion) to explicit
  confirmation.
- Keep `CLAUDE.md` accurate as the agent's source of project truth: Django
  version-pinning guidance, layered conventions (`services.py`/`selectors.py`,
  thin views), and the "easy to break" checklist stay current with the planned
  stack.
- Add optional, opt-in Claude Code hooks that run `ruff format` / `ruff check`
  automatically so formatting/lint stays green without manual cycles.
- No application/runtime code changes; this is tooling and agent-configuration
  only.

## Capabilities

### New Capabilities
- `agent-permissions`: The project's committed allow/deny policy for which
  commands the agent may run unattended versus which always require confirmation.
- `agent-project-context`: The maintained guardrails in `CLAUDE.md` (stack
  versions, layering conventions, change-coupling and break-risk checklists) that
  give the agent reliable, current project context.
- `dev-automation-hooks`: Opt-in Claude Code hooks that automate lint/format so
  the codebase stays consistent without manual steps.

### Modified Capabilities
<!-- None: no existing specs in openspec/specs/. -->

## Impact

- New file: `.claude/settings.json` (committed, shared with collaborators).
- Updated file: `CLAUDE.md` (already partially refined: Django 6.0.x / LTS 5.2.x
  version note added).
- Optional new file: `.claude/settings.json` hooks section (or
  `.claude/settings.local.json` for personal-only hooks).
- No changes to `pyproject.toml` dependencies, `main.py`, or any runtime code.
- Affects developer/agent workflow only; no user-facing behavior.
