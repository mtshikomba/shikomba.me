# task-025: Add intro, projects showcase, and resume to the website

## User story

As a visitor to `shikomba.me`, I want to quickly read a short introduction about the owner, browse past and ongoing projects (including open-source work), and view or download a resume so that I can evaluate the owner's background and experience without leaving the site.

## Problem

The site (task-024) currently scopes only a blog and a generic about/bio page. There is no dedicated projects showcase, no resume/CV presentation, and no downloadable resume file or route.

## Scope

Extend the Django site from task-024 with a short intro section, a projects showcase, and a resume page.

### In scope

- Short introduction: a concise bio/summary of the owner shown on the home page or a dedicated section, distinct from the longer about page in task-024.
- Projects app/model: title, short description, role, status (`ongoing`/`completed`), technology tags, optional source-code URL, optional live-demo URL, optional open-source flag, and optional date range.
- Projects list view showing ongoing and past projects, clearly distinguishing status, with open-source projects visibly marked and linking out to their repositories.
- Resume page: renders the resume content on-site (structured sections such as experience, education, skills) and provides a "Download resume" action serving a PDF file.
- Resume content and the downloadable PDF are managed by the owner (via Django admin or a single configured file), not publicly editable.
- Downloadable resume is served as an actual file download (correct `Content-Disposition`/content type), not a broken or placeholder link.
- Navigation updated to surface Blog, Projects, Resume, and About/Intro as primary links.
- Responsive layout for the intro section, projects list, and resume page at mobile and desktop widths.

### Out of scope

- Full custom visual design system (tracked separately, same as task-024).
- Project detail pages beyond the list view, unless the product owner requests them in a follow-up.
- Auto-generating the resume PDF from structured data; a maintained static PDF is acceptable for this ticket.
- Blog implementation itself (tracked in task-024).

## Acceptance criteria

- [ ] The home page (or a dedicated intro section) displays a short, current introduction about the owner.
- [ ] A projects route lists all published projects, showing title, short description, status (`ongoing`/`completed`), and technology tags for each.
- [ ] Open-source projects are visibly marked and link to their source-code repository; non-open-source projects do not show a source-code link if none is configured.
- [ ] Projects with a live-demo URL show a working link; projects without one do not display a broken or placeholder link.
- [ ] A resume route renders resume content (experience, education, skills) directly on the page.
- [ ] The resume page includes a "Download resume" control that serves an actual PDF file with correct content type and filename.
- [ ] Projects and resume content are editable only through Django admin or an equivalent authenticated interface; there is no public-facing edit access.
- [ ] Primary navigation includes working links to Projects, Resume, and the intro/about content alongside the existing Blog link from task-024.
- [ ] At viewport widths of 375px and 1440px, the projects list and resume page have no horizontal scrolling and remain readable.
- [ ] Focused automated tests cover: projects list renders only published projects, open-source marking/link logic, resume page renders expected sections, and the resume download returns the correct content type.

## Implementation notes

- Reuse the Django project and conventions established in task-024; add a `projects` app and a `resume` app/module rather than overloading the `blog` app.
- Store the resume PDF as a versioned static/media asset referenced by settings or a single admin-managed field, following the repository's file-handling and security conventions.
- Depends on task-024 being in progress or completed for the base project scaffold, settings, and templates.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused Python tests pass, `python manage.py check` passes, and flake8/black checks pass on changed files.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
