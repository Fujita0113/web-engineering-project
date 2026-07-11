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

## Note on the User Interface

The main screen is a vertical feed of posts, newest first, each showing the title, author name, date, and a part of the text. Author names are links to that author's posts. A date filter lets the user pick a day. Next and Previous links are shown for pagination. In the header there is a login and register area; when logged in, a form for a new post (title and text) is available.
