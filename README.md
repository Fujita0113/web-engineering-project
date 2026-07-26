# Project Proposal - Exercise 2: The Blogs

## Project Title

The Blogs - A Shared Blogging Platform

## Short Description

A web application where registered users write their own text posts in one shared space, and everyone can read them. It has a browser UI, server-side logic (login, filtering, pagination), and a database for users and posts.

## Main User Actions

1. Display all blog posts sorted by date, the newest first.
2. Display the list of authors.
3. Display only the posts written by a selected author.
4. Select a date in the calendar and display all posts written on that day.
5. Register with a unique user name and password, and start writing own posts.

The system shows no more than P posts per page, with Next and Previous links.

## Basic Data Model Idea

Two entities:

- **Author (user)**: id, user name (unique), password.
- **Post**: id, title, text content, creation date, and the author who wrote it.

One author has many posts; one post belongs to one author. At the start the database has up to 5 authors and up to 20 posts.

---

## Main Data Entities

| Table | Columns |
|-------|---------|
| **Users** | id, username (unique), password, date_joined |
| **Posts** | id, title, content, created_at, author_id (FK → Users) |

Implemented as a custom `accounts.User` model (extends Django's `AbstractUser`),
so `date_joined` serves as the account creation timestamp and `password` is
stored hashed. `Posts.created_at` is set automatically on creation, and posts
are ordered newest-first.

**Relationships:**  
One User has many Posts (1:N)

---

## Main User Flow

### Unregistered User
1. Home → See all posts (sorted by date, newest first)
2. Click author name → See posts by that author
3. Select date from calendar → See posts from that day
4. Next/Previous links → Navigate pages
5. Click "Register" → Enter username & password → Account created

### Registered User
1. Home → See all posts
2. [Same filtering options: author, date, pagination]
3. Logged in → Write new post form appears
4. Enter title & text → Submit → Post created

---

## Architecture Sketch

```
┌────────────────────┐
│   WEB BROWSER      │
│ • Post feed        │
│ • Filters          │
│ • Pagination       │
│ • Login/Register   │
└─────────┬──────────┘
          │ HTTP Request/Response
          ↓
┌────────────────────┐
│  DJANGO SERVER     │
│ • Routes           │
│ • Views (filter,   │
│   sort, paginate)  │
│ • Auth             │
│ • Models           │
└─────────┬──────────┘
          │ SQL Query/Result
          ↓
┌────────────────────┐
│   DATABASE         │
│ • Users            │
│ • Posts            │
└────────────────────┘
```

---

## API (URLs) — Exercises 6 & 8

View functions wired in `blog/urls.py` (included at the site root). Pages render
minimal HTML templates (`blog/templates/`, extending `base.html`). Author search
takes real user input via a GET form (Exercise 8 replaced the hard-coded stub).

| Method & URL | View | Arguments | Returns |
|--------------|------|-----------|---------|
| `GET /` | `blog.views.post_list` | none | HTML list of all posts, newest first; author names link to their posts |
| `GET /authors/` | `blog.views.author_list` | none | HTML list of authors, each linking to their posts |
| `GET /by-author/` | `blog.views.posts_by_author` | `author` (query string, e.g. `?author=alice`) | Search form + that author's posts; with no `author`, only the form. Unknown author shows "no posts found" |

All three return an HTML `HttpResponse` rendered from templates.

Not implemented yet (later exercises): pagination, date filter, authentication,
and POST forms (registration, login, post creation).

---

## Note on the User Interface

The main screen is a vertical feed of posts, newest first, each showing the title, author name, date, and a part of the text. Author names are links to that author's posts. A date filter lets the user pick a day. Next and Previous links are shown for pagination. In the header there is a login and register area; when logged in, a form for a new post (title and text) is available.

---

## Deployment — Exercise 11

### Production decisions

| Question | Decision |
|----------|----------|
| Hosting | [Render.com](https://render.com/) Free Web Service |
| Application server | `waitress` (WSGI) |
| Static files (CSS/JS) | `whitenoise`, with `collectstatic` run at build time and `CompressedManifestStaticFilesStorage` in production |
| Uploaded/media files | Not applicable — no `FileField`/`ImageField` exists in the current models (`Users`, `Posts`) |
| Database | SQLite for local development; Postgres (Render Free instance, via `dj-database-url` + `DATABASE_URL`) in production, since Render's Free web service disk is ephemeral |

### Environment variables (production)

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `False` |
| `ALLOWED_HOSTS` | Comma-separated hostnames (Render also auto-provides `RENDER_EXTERNAL_HOSTNAME`) |
| `DATABASE_URL` | Set automatically by Render when a Postgres instance is attached |

### Deploy steps (Render.com)

1. Push this repository to GitHub (already the case).
2. In the Render dashboard, create a **PostgreSQL** instance (Free tier).
3. Create a **Web Service** from this GitHub repo:
   - Build command: `bash build.sh`
   - Start command: `bash run.sh`
   - Add env vars `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS` (or rely on `RENDER_EXTERNAL_HOSTNAME`)
   - Attach the Postgres instance so `DATABASE_URL` is set automatically
4. Deploy. `build.sh` runs `uv sync`, `collectstatic`, and `migrate`; `run.sh` starts `waitress-serve`.

### Local production-mode smoke test

```pwsh
$env:DEBUG = "False"
$env:ALLOWED_HOSTS = "127.0.0.1"
$env:SECRET_KEY = "local-test-secret"
uv run python manage.py collectstatic --no-input
uv run python manage.py migrate
uv run waitress-serve --port=8000 config.wsgi:application
```
