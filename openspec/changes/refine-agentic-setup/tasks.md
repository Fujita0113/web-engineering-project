## 1. Permission policy (agent-permissions)

- [x] 1.1 Create `.claude/settings.json` with a `permissions.allow` array
- [x] 1.2 Allowlist safe dev commands: `uv sync`, `uv add`, `uv run pytest`,
      `uv run ruff`, `uv run python manage.py`
- [x] 1.3 Allowlist read-only/additive git: `status`, `diff`, `log`, `show`,
      `branch`, `add`
- [x] 1.4 Verify `commit`/`push`/`reset` and deletions are NOT allowlisted
- [x] 1.5 Validate the file parses as JSON

## 2. Project context guardrails (agent-project-context)

- [x] 2.1 Add Django version-pinning guidance to `CLAUDE.md` (stable 6.0.x /
      LTS 5.2.x + reconfirm-and-pin instruction)
- [ ] 2.2 Confirm layering conventions (`services.py`/`selectors.py`/thin views)
      are present and accurate in `CLAUDE.md`
- [ ] 2.3 Confirm "easy to break" and "change coupling" checklists are present
      and current in `CLAUDE.md`

## 3. Lint/format automation (dev-automation-hooks)

- [ ] 3.1 Decide opt-in mechanism (Stop hook in `settings.json` vs personal
      `settings.local.json`)
- [ ] 3.2 Document the hook: `uv run ruff format` + `uv run ruff check`, off by
      default, no git-write/delete actions
- [ ] 3.3 (If enabled) add the hook config and confirm it only formats/reports

## 4. Verification & commit

- [ ] 4.1 Run `uv run ruff check .` and `uv run ruff format --check .` to confirm
      the setup does not break existing tooling
- [ ] 4.2 Review `git status` / `git diff` for the agentic-setup files
- [ ] 4.3 Commit `.claude/settings.json` and `CLAUDE.md` changes (with user
      confirmation)
