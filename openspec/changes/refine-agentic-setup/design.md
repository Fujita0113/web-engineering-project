## Context

The repo is a Django course project still at the skeleton stage (only `main.py`,
`uv`, `pytest`, `ruff`). It already carries strong context — a project
`CLAUDE.md`, a global `CLAUDE.md` (version-pinning, pwsh, skill-placement
policies), global Django skills, and OpenSpec — but had no committed agent
operating configuration. Two pieces were already applied in-session:
`.claude/settings.json` with a permission allowlist, and a Django version note in
`CLAUDE.md`. This design captures the full shape so the change can be reviewed and
finished coherently rather than as ad-hoc edits.

Constraints: Windows + pwsh environment; `uv` is the package manager; the project
guideline favors minimal artifacts; irreversible operations must stay
user-confirmed.

## Goals / Non-Goals

**Goals:**

- A committed, predictable permission policy: safe dev commands run unattended,
  irreversible ones always prompt.
- `CLAUDE.md` remains the accurate source of project truth (version policy,
  layering, break-risk/coupling checklists).
- Provide an *opt-in* lint/format automation hook, documented but off by default.

**Non-Goals:**

- Installing Django or writing any application/runtime code.
- Adding custom subagents or project-local skills — global `django-expert` /
  `django-patterns` skills already cover that; duplicating them wastes context.
- Personal/machine-specific config (belongs in `settings.local.json`, untracked).

## Decisions

- **Commit `.claude/settings.json`, not `.local.json`, for the allowlist.**
  The permission policy should be shared and reviewable by collaborators.
  Personal overrides remain possible via `settings.local.json` (git-ignored).
  Alternative considered: local-only settings — rejected because it gives each
  collaborator divergent, invisible behavior.

- **Allowlist by command prefix, scoped narrowly.** Allow `uv run pytest`,
  `uv run ruff`, `uv run python manage.py`, and read-only/additive git
  (`status`, `diff`, `log`, `show`, `branch`, `add`). Stop at `git add` —
  `commit`/`push`/`reset` stay prompted. Alternative: broad `Bash(git:*)` —
  rejected as too permissive for irreversible subcommands.

- **Keep the version-pinning policy in `CLAUDE.md`, reconfirmed at install
  time.** Record current stable (6.0.x) / LTS (5.2.x) as a hint, but require a
  fresh PyPI check and a pinned `>=` constraint before `uv add django`.
  Alternative: pin a fixed version now — rejected because Django is not yet
  installed and the latest stable may move before implementation.

- **Make the lint/format hook opt-in.** A `Stop`/post-edit hook running
  `uv run ruff format` + `uv run ruff check` keeps the tree clean, but
  auto-running tools can surprise a learning user. Document it and let the user
  enable it deliberately. Alternative: enable by default — rejected for a course
  project where transparency matters more than automation.

## Risks / Trade-offs

- **[Allowlist drifts from real workflow]** → Revisit when Django is added (e.g.
  `manage.py test` is already covered by the `manage.py` prefix; no change
  needed).
- **[`uv add` is allowlisted and mutates `pyproject.toml`]** → Acceptable: it is
  reversible via VCS and is core to dev flow; the actual dependency choice still
  goes through the version-pinning policy.
- **[Opt-in hook is forgotten / never enabled]** → Acceptable; `ruff` can always
  be run manually via the documented commands, and CI/test expectations are
  unaffected.
- **[settings.json committed with a machine-specific quirk]** → Mitigated by
  keeping only portable command-prefix rules in the committed file.
