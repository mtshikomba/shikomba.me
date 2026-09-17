# task-025: Add intro, projects showcase, and resume to the website

## User story

As a visitor to `shikomba.me`, I want to quickly read a short introduction about the owner, browse past and ongoing projects (including open-source work), and view or download a resume so that I can evaluate the owner's background and experience without leaving the site.

## Problem

The site (task-024) currently scopes only a blog and a generic about/bio page. There is no dedicated projects showcase, no resume/CV presentation, and no downloadable resume file or route.

## Scope

Extend the Django site from task-024 with a short intro section, a projects showcase, and a resume page.

### In scope

- Short introduction: a concise bio/summary of the owner shown on the home page or a dedicated section, distinct from the longer about page in task-024.
- Projects app/model: title, short description, role, status (`ongoing`/`completed`), technology tags (stored as a simple comma-separated `CharField`, not a new third-party tagging dependency), optional source-code URL, optional live-demo URL, optional open-source flag, and optional date range.
- Projects list view showing ongoing and past projects, clearly distinguishing status, with open-source projects visibly marked and linking out to their repositories.
- Resume app with a single admin-managed `Resume` model (one editable row) holding structured content (experience, education, skills) and a `FileField` for the PDF upload; no template-hardcoded resume content.
- Resume page: renders the resume content on-site and provides a "Download resume" action that streams the `FileField` via Django's storage API (e.g. `FileResponse`), never a request-supplied filesystem path.
- Resume PDF uploads are validated server-side on save: `.pdf` extension only, MIME/content-sniffed as `application/pdf`, and capped at a maximum file size (5MB) to prevent unrestricted file upload.
- Resume content and the downloadable PDF are managed by the owner (via Django admin), not publicly editable.
- Navigation updated to surface Blog, Projects, Resume, and About/Intro as primary links.
- Responsive layout for the intro section, projects list, and resume page at mobile and desktop widths.

### Out of scope

- Full custom visual design system (tracked separately, same as task-024).
- Project detail pages beyond the list view, unless the product owner requests them in a follow-up.
- Auto-generating the resume PDF from structured data; a maintained static PDF is acceptable for this ticket.
- Blog implementation itself (tracked in task-024).

## Acceptance criteria

- [x] The home page (or a dedicated intro section) displays a short, current introduction about the owner.
- [x] A projects route lists all published projects, showing title, short description, status (`ongoing`/`completed`), and technology tags for each.
- [x] Open-source projects are visibly marked and link to their source-code repository; non-open-source projects do not show a source-code link if none is configured.
- [x] Projects with a live-demo URL show a working link; projects without one do not display a broken or placeholder link.
- [x] A resume route renders resume content (experience, education, skills) directly on the page from the single admin-managed `Resume` record.
- [x] The resume page includes a "Download resume" control that streams the stored `FileField` via Django's storage API with correct content type and filename.
- [x] Uploading a non-PDF file or a PDF exceeding the size limit as the resume is rejected server-side with a clear admin-facing error.
- [x] Projects and resume content are editable only through Django admin or an equivalent authenticated interface; there is no public-facing edit access.
- [x] Primary navigation includes working links to Projects, Resume, and the intro/about content alongside the existing Blog link from task-024.
- [x] At viewport widths of 375px and 1440px, the projects list and resume page have no horizontal scrolling and remain readable.
- [x] Focused automated tests cover: projects list renders only published projects, open-source marking/link logic, resume page renders expected sections, resume download returns the correct content type, and oversized/non-PDF resume uploads are rejected.

## Implementation notes

- Reuse the Django project and conventions established in task-024; add a `projects` app and a `resume` app/module rather than overloading the `blog` app.
- Add `MEDIA_ROOT`/`MEDIA_URL` to `config/settings.py` and serve media locally in development for the resume `FileField`.
- Validate the resume upload in the model's `clean()`/`save()` or a form validator: extension, sniffed content type, and size limit — do not rely on client-side `accept` attributes alone.
- Depends on task-024, which is complete, for the base project scaffold, settings, and templates.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused Python tests pass, `python manage.py check` passes, and flake8/black checks pass on changed files.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
