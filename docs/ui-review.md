# UI Review — Ex9

Review of the current interface (`blog/templates/`) against the four Ex9
criteria. Scope: `base.html`, `blog/post_list.html`, `blog/author_list.html`,
`blog/posts_by_author.html`. No CSS or `static/` assets exist yet.

Legend: ✅ ok · ⚠️ partial · ❌ missing

---

## 1. HTML organized in a clean and logical way — ⚠️

**Current state:** `base.html` uses template inheritance and the semantic
landmarks `<header>`, `<nav>`, `<main>`. Heading order is logical
(`h1` site title → `h2` page → `h3` sub-section). Page `<title>` is set per page.

**Findings:**

- **F1.** `<hr>` in `base.html` is a presentational separator — visual styling
  belongs in CSS (`border`/`padding`), not in the markup.
- **F2.** Nav links are joined by literal ` | ` text between anchors. A list of
  links should be marked up as a `<ul>`/`<li>`; the separators are presentation.
- **F3.** Post/author listings use `&mdash;` and `<strong>` inline to fake a
  layout (date — title). The visual separation should come from CSS, and
  `<strong>` here is styling a title, not marking importance.
- **F4.** No skip-to-content link before the nav (structural affordance for
  keyboard users; also an accessibility item — see §4).

## 2. CSS separates structure from presentation — ❌

**Current state:** There is **no CSS file and no `{% static %}` link** anywhere.
`base.html` has no `<link rel="stylesheet">`. All appearance currently relies on
browser default styles plus the in-HTML hacks noted in F1–F3.

**Findings:**

- **F5.** Create `blog/static/blog/style.css` and load it in `base.html` via
  `{% load static %}` + `<link rel="stylesheet" href="{% static ... %}">`.
  This is the core requirement of criterion 2.
- **F6.** Once CSS exists, remove the presentational markup (F1–F3) and express
  it as styles (separator borders, list layout, spacing).

## 3. Responsive — ❌

**Current state:** No `<meta name="viewport">` and no layout CSS. On a phone the
page renders at desktop width and zooms out; content is not designed to reflow.

**Findings:**

- **F7.** Add `<meta name="viewport" content="width=device-width, initial-scale=1">`
  to `base.html` `<head>` — without it, mobile browsers do not use CSS breakpoints.
- **F8.** Give `<main>` a fluid max-width container (e.g. `max-width` + `margin
  auto` + relative units) so lines don't stretch full-width on desktop while
  still filling small screens. A simple `@media` breakpoint is enough to
  demonstrate the criterion.

## 4. Accessible — ⚠️

**Current state:** `lang="en"` is set, `charset` is declared, headings are
ordered, and the submit control is a real `<button>`. Good baseline.

**Findings:**

- **F9.** The author search `<input>` in `posts_by_author.html` has only a
  `placeholder`, no `<label>`. Placeholder text is not an accessible name and
  disappears on input. Add a `<label for=...>` (visually hidden if desired).
- **F10.** No skip link (see F4) — keyboard users must tab through the nav on
  every page.
- **F11.** With two future navs possible, the primary `<nav>` should carry an
  `aria-label` (e.g. `"Primary"`) to disambiguate for screen readers. Minor now.
- **F12.** When CSS/colors are introduced (§2/§3), verify text/background
  contrast meets WCAG AA (4.5:1). Nothing to fix yet, but constrain the palette
  when styling.

---

## Summary → improvement backlog

| # | Criterion | Fix | Priority |
|---|-----------|-----|----------|
| F5 | CSS separation | Add `static/blog/style.css` + `{% static %}` link | High |
| F7 | Responsive | Add viewport meta | High |
| F9 | Accessible | Label the search input | High |
| F1–F3, F6 | Clean HTML / CSS | Remove `<hr>`/`|`/`&mdash;` hacks, move to CSS | Medium |
| F2 | Clean HTML | Nav as `<ul>` list | Medium |
| F8 | Responsive | Fluid max-width container + one breakpoint | Medium |
| F4/F10 | Accessible | Skip-to-content link | Medium |
| F11 | Accessible | `aria-label` on primary nav | Low |
| F12 | Accessible | Check contrast when styling | Low (verify) |

These findings drive the follow-up improvement issue.
