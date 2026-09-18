# task-027: Add published research archive

## User story

As a visitor to `shikomba.me`, I want to browse the owner's published research work so that I can understand their research interests and access relevant papers, articles, or reports.

## Problem

The website currently showcases blog posts, projects, and a resume, but it has no dedicated area for published research work.

## Scope

Add a public research archive backed by Django and managed through the existing admin interface.

### In scope

- Add a `research` app with a `Research` model containing title, abstract/summary, publication date, publication URL, and published/draft status.
- Add an admin interface for creating, editing, publishing, unpublishing, and deleting research entries.
- Add a public `/research/` list page showing published research ordered newest first.
- Display each entry's title, publication date, summary, and a working link to the full publication.
- Add a Research link to the public primary navigation and indicate the active page.
- Reuse the existing public CSS design system and responsive layout.

### Out of scope

- Public research submission or editing.
- Search, filtering, comments, citations management, or analytics.
- Uploading and hosting research files; publications may link to an external repository or already-hosted document.
- Changes to the Django admin visual design.

## Acceptance criteria

- [x] A `research` Django app exists with migrations and a `Research` model containing title, summary, publication date, publication URL, and published/draft status.
- [x] Admin users can create, edit, publish/unpublish, and delete research entries.
- [x] `/research/` returns a successful response and lists published research entries newest first.
- [x] Draft or unpublished research entries never appear on the public research page.
- [x] Each listed entry shows its title, formatted publication date, summary, and a valid `Read publication` link using its configured URL.
- [x] The primary navigation includes a working Research link and identifies it as the current page on `/research/`.
- [x] The research page uses the shared public styles and has no horizontal scrolling at 375px or 1440px.
- [x] The page has logical heading structure, visible keyboard focus, and accessible link text.
- [x] Focused automated tests cover published-only visibility, newest-first ordering, rendering of publication metadata/link, and the research route.
- [x] Existing tests continue to pass, `python manage.py check` passes, and black/flake8 checks pass.

## Implementation notes

- Follow the existing app structure used by `blog`, `projects`, and `resume`: models, admin, views, URLs, migrations, and templates under the app.
- Add the route without changing existing URL names or public behavior.
- Reuse `static/css/site.css` and existing `card`/`card-meta` classes; do not introduce a second public styling system.
- Use explicit type hints and Google-style docstrings for new public Python functions and classes.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused and full test suites pass.
- Browser validation covers the research page at mobile and desktop widths.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
