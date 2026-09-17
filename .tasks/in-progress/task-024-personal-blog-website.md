# task-024: Launch personal blog website at shikomba.me

## User story

As the site owner, I want a personal blog hosted at `shikomba.me` and built on a Django backend so that I can publish posts, share an about/bio page, and let visitors find and read my writing reliably on any device.

## Problem

No website currently exists for the `shikomba.me` domain. There is no Django project scaffold, no content model for posts, and no defined deployment or hosting target for the domain.

## Scope

Stand up a new Django-backed personal blog project intended to be deployed at `shikomba.me`.

### In scope

- New Django project and a `blog` app with models for posts (title, slug, body, publish date, published/draft status) and an about/bio page.
- Public views: home/post list (paginated), post detail by slug, about page, and a simple tag or category filter if categories are introduced.
- Admin-only authoring: use Django admin (or an equivalent authenticated interface) to create, edit, publish/unpublish, and delete posts. No public-facing post creation.
- Basic SEO/plumbing: page titles, meta description per post, `robots.txt`, and an XML sitemap.
- Responsive, accessible base template usable on mobile and desktop; no specific visual brand direction is mandated yet.
- Environment-based configuration (`.env`, not committed) for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and database settings, per repository security baseline.
- Domain and hosting target: the site must be configured to serve correctly when `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` include `shikomba.me` and `www.shikomba.me`. Actual DNS/hosting-provider setup is out of scope for this ticket unless the product owner supplies provider details.

### Out of scope

- Comments, newsletter signup, or social sharing integrations.
- Multi-author support or user-facing registration.
- Full custom visual design system (colors, typography) — a follow-up UX ticket will define this once content scope is confirmed.
- CI/CD pipeline and production infrastructure provisioning (tracked separately if needed).

## Acceptance criteria

- [x] A Django project runs locally via the repository's standard test/run tooling and `python manage.py check` passes with no errors.
- [x] Visiting the home route shows a paginated list of published posts only; draft posts never appear in public views.
- [x] Each published post has a working detail route reachable from the list by its slug, returning a 404 for unknown slugs and for unpublished posts.
- [x] An about/bio page is reachable from the site's primary navigation.
- [x] Posts can be created, edited, and published/unpublished through Django admin without direct database or shell access.
- [x] `robots.txt` and an XML sitemap are served and list only published content.
- [x] `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and database credentials are read from environment variables/`.env` and are not hardcoded or logged.
- [x] `ALLOWED_HOSTS` and CSRF trusted origins are configured to accept `shikomba.me` and `www.shikomba.me` in production settings.
- [x] At viewport widths of 375px and 1440px, the home, post detail, and about pages have no horizontal scrolling and remain readable.
- [x] Focused automated tests cover: post list only shows published posts, post detail 404s for drafts/unknown slugs, about page renders, and sitemap/robots respond successfully.

## Implementation notes

- Keep Django settings split or environment-driven so local development and production hosting differ only by environment variables.
- Follow repository conventions once implementation begins: PEP 8, explicit type hints on public functions/methods, Google-style docstrings for new public modules/classes.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused Python tests pass, `python manage.py check` passes, and flake8/black checks pass on changed files.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
