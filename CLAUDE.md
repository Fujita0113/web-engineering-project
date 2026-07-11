# CLAUDE.md

## Project scope

"The Blogs" — a shared blogging platform where registered users write text posts
in one shared space. It consists of a browser UI, server-side logic
(authentication, filtering, pagination), and a database.

### Current state

Runnable Django project with the database schema in place. `config/` holds the
project settings, and two apps (`accounts`, `blog`) define the `User` and `Post`
models. Migrations are created and applied (SQLite). Views/templates are not
built yet.

## Tech stack

- Python 3.12+ (managed via `.python-version`)
- Package manager: **uv**
- Framework: Django 6.0.7 (pinned `Django>=6.0,<7.0` in `pyproject.toml`)
  - Requires Python 3.12+. Re-check the latest patch before upgrading and keep
    the major upper bound pinned with `<7.0`.
- Testing: pytest / pytest-cov
- Linter / Formatter: ruff

## Data model

| Table     | Columns                                              |
|-----------|------------------------------------------------------|
| **Users** | id, username (unique), password, date_joined         |
| **Posts** | id, title, content, created_at, author_id (FK)       |

Relationship: User 1 : N Post

- `Users` is a custom model `accounts.User` extending `AbstractUser`
  (`AUTH_USER_MODEL = 'accounts.User'`); `date_joined` is the creation timestamp
  and `password` is stored hashed.
- `Posts` lives in the `blog` app; `created_at` uses `auto_now_add`, and the
  default ordering is newest-first (`ordering = ['-created_at']`).

## App structure

- `config/` — project settings, root URLconf, WSGI/ASGI entry points
- `blog/` — `Post` model (done); post feed, author filter, date filter,
  pagination (planned)
- `accounts/` — custom `User` model (done); user registration, login, logout
  (planned)

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
