# CLAUDE.md

## Project scope

"The Blogs" — a shared blogging platform where registered users write text posts
in one shared space. It consists of a browser UI, server-side logic
(authentication, filtering, pagination), and a database.

### Current state

A skeleton without Django yet. Only `main.py` and dev tools (pytest / ruff) exist.

## Tech stack

- Python 3.12+ (managed via `.python-version`)
- Package manager: **uv**
- Framework: Django (not yet installed; planned)
  - 最新安定版 6.0.x / LTS 5.2.x（PyPI 確認: 2026-06-24 時点）。
    導入時は `uv add` 直前に最新版を再確認し、`>=` でメジャー上限を固定すること。
- Testing: pytest / pytest-cov
- Linter / Formatter: ruff

## Data model

| Table     | Columns                                          |
|-----------|--------------------------------------------------|
| **Users** | id, username (unique), password, created_at      |
| **Posts** | id, title, content, created_at, author_id (FK)   |

Relationship: User 1 : N Post

## App structure (planned, once Django is added)

- `blog/` — post feed, author filter, date filter, pagination
- `accounts/` — user registration, login, logout

## Commands

```pwsh
# Install dependencies
uv sync

# Start the Django dev server (after Django is added)
uv run python manage.py runserver

# Create and apply migrations (after Django is added)
uv run python manage.py makemigrations
uv run python manage.py migrate

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Lint / format checks
uv run ruff check .
uv run ruff format --check .
```

## Conventions

- Put business logic (filtering, pagination math, etc.) in `services.py`.
- Put query/read logic in `selectors.py`.
- Keep views thin (only request/response translation).
- Do not edit existing migrations; create a new one instead.

## Things that are easy to break

- Pagination boundaries (empty result, last page)
- Combining the author filter with the date filter
- Hiding the post form from unauthenticated users
- URL names (referenced from templates via `{% url %}`)

## Change coupling

- Change a model → also check migrations, forms, and templates
- Change auth logic → also check login-required view decorators
- Change a URL name → also check `{% url %}` tags in templates

## Testing expectations

Add or update tests for:

- Post feed (all posts, author filter, date filter)
- Pagination (including boundary values)
- User registration, login, logout
- Rejecting post actions from unauthenticated users
