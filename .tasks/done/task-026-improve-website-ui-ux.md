# task-026: Improve the website's UI/UX

## User story

As a visitor to `shikomba.me`, I want the blog, projects, resume, and about pages to feel cohesive, polished, and easy to use on any device so that I trust the site and can navigate it comfortably.

## Problem

The current site (task-024, task-025) is functional but visually minimal: shared styling lives as inline CSS in `templates/base.html`, there is no defined color/typography system, and no accessibility or responsive pass has been done beyond basic mobile-width checks during implementation. Pages are plain and inconsistent in visual hierarchy across the blog, projects, and resume sections.

## Scope

Improve the shared visual design and accessibility of the existing Django templates without changing URL names, models, views, or form/submission behavior.

### In scope

- Establish a cohesive visual system in `templates/base.html`: typography, color palette, spacing, link/button states, and navigation styling, moved into a proper static stylesheet under a shared `static/` directory instead of inline `<style>` in the template.
- Improve visual hierarchy on the home page (intro + post list), post detail, about, projects list, and resume pages.
- Make the primary navigation clearly show the current page, be keyboard accessible, and work without horizontal overflow on narrow screens.
- Add pagination, empty-state, and list styling improvements for the post list and projects list.
- Improve the projects list to visually distinguish `ongoing`/`completed` status and open-source markers.
- Improve the resume page layout (experience/education/skills sections, download action) for readability.
- Ensure sufficient color contrast (WCAG AA), visible keyboard focus states, and correct heading order (one `h1` per page).
- Add responsive layout support for mobile (375px) and desktop (1440px) widths across all existing pages.

### Out of scope

- Changing Django models, views, URL names, or form/submission behavior.
- Adding new content sections, models, or fields beyond what task-024/task-025 already introduced.
- The Django admin interface (`/admin/`) is out of scope; this ticket covers public-facing pages only.

## UX specification

### Color palette

| Token | Value | Use |
| --- | --- | --- |
| `--ink` | `#1F2937` | Body text, headings, footer |
| `--paper` | `#FAFAF9` | Page background |
| `--surface` | `#FFFFFF` | Cards, content panels |
| `--line` | `#E5E7EB` | Borders, dividers |
| `--brand` | `#2563EB` | Links, primary actions, active nav state |
| `--brand-dark` | `#1D4ED8` | Hover/pressed link and button states |
| `--muted` | `#6B7280` | Secondary text (meta, dates), still AA-compliant on `--paper` |
| `--success` | `#15803D` | "Ongoing"/open-source status markers |
| `--neutral-status` | `#4B5563` | "Completed" status marker |

Rules: use `--ink`/`--paper` as the structural pair; `--brand` is the single accent for links and active states; status/open-source markers pair an icon or label text with color, never color alone.

### Typography

- System font stack (no webfont dependency): `-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.
- Base body size `1rem`, line height `1.6`. Headings use `font-weight: 700`; body copy uses regular weight.
- `h1` reserved for the page's single top-level heading; `h2` for section/article titles.

### Component notes

- Buttons/links: `--brand` text or fill with white text, `--brand-dark` on hover/focus; 3px visible focus outline offset from the element.
- Small rounded corners (4px), a single subtle border/shadow for cards (post list items, project cards, resume sections) — avoid heavy shadows or pill shapes.
- Status badges (ongoing/completed) and the open-source marker use a label plus a small icon or distinct border style, not color alone, to meet non-color-dependent state requirements.

## Acceptance criteria

- [x] Shared styles live in a static stylesheet (not inline `<style>` in `base.html`) and are used consistently across all pages.
- [x] All existing routes continue to return successful responses: home, post detail, about, projects list, and resume.
- [x] Primary navigation visually and programmatically identifies the current page and is operable by keyboard.
- [x] At 375px and 1440px viewport widths, the home, post detail, about, projects, and resume pages have no horizontal scrolling and no clipped or overlapping content.
- [x] Text and interactive elements meet WCAG AA contrast (4.5:1 normal text, 3:1 large text/controls); focus states are visible on all interactive elements.
- [x] Each page has exactly one `h1` and a logical heading order.
- [x] Projects list visually distinguishes `ongoing` vs `completed` status and marks open-source projects without relying on color alone.
- [x] Existing automated tests continue to pass with no changes to their assertions about page content/behavior (only presentation changes).
- [x] The Django admin interface is untouched; only public-facing templates and static assets are changed.
- [x] The implemented styling uses the documented color palette and typography from the UX specification above.

## Implementation notes

- Add a `static/` directory (already referenced conditionally in `config/settings.py` `STATICFILES_DIRS`) with a single shared CSS file linked from `templates/base.html`.
- `STATICFILES_DIRS` is evaluated once at process start (`[BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []`), so create the `static/` directory before starting the dev server, or restart the server after creating it, or the new stylesheet won't be picked up.
- `STATIC_ROOT`/`collectstatic` are not configured yet; that's out of scope here and tracked as a fast-follow once production deployment is scoped.
- Keep template block structure (`title`, `meta_description`, `content`) intact so per-page templates don't need structural rewrites.
- Follow repository conventions: PEP 8, docstrings for any new Python code, and run `black`/`flake8` on any touched files.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused Python tests pass, `python manage.py check` passes, and flake8/black checks pass on changed files.
- Browser validation recorded at 375px and 1440px for all affected pages.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
