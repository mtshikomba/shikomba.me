# task-035: Update About-page bio

## User story

As a visitor to shikomba.me, I want the About page to present an accurate professional bio so I can understand Matheus Tangeni Shikomba's experience, technical expertise, research, and education.

## Problem

The About page currently displays a short placeholder description: "I'm Matheus T. Shikomba, a software engineer and researcher." It does not reflect the approved professional bio and its additional details about leadership, technology, research, and education.

## Scope

Replace the current About-page bio with the user-provided professional bio exactly as supplied:

> Matheus Tangeni Shikomba is a Full-Stack Software Engineer and Scrum Master at Logic Solutions Inc., where he leads agile development teams and builds scalable enterprise applications. His expertise includes Python for data science, Django, PHP, Symfony, Laravel, Vue.js, Angular, RESTful APIs, AI, database optimization, and cloud infrastructure. He is also a published ACM Natural Language Processing researcher. Matheus holds an MS in Computer Science from Eastern Michigan University and a BS in Computer Science with Honors from the University of Namibia.

### In scope

- Update the About-page bio copy with the approved text.
- Preserve the existing About-page heading, profile image, contact links, layout, navigation, and routes.
- Add focused automated coverage asserting the approved bio is rendered.
- Preserve readable paragraph structure and responsive behavior.

### Out of scope

- Changing the site's visual design, typography, or layout.
- Changing the resume, project, research, or blog content.
- Changing Django models, views, URLs, admin behavior, or migrations.
- Adding claims, links, credentials, or details not present in the supplied text.

## Acceptance criteria

- [x] The About page renders the supplied professional bio verbatim, including the listed technologies, employer, research description, and degrees.
- [x] The old placeholder bio is removed from the About page.
- [x] The page retains exactly one `h1`, the profile image and alt text, existing contact links, header navigation, and footer links.
- [x] No unsupported claims or additional content are introduced.
- [x] The bio remains readable without clipping, overlap, or horizontal scrolling at 375px and 1440px.
- [x] Focused automated coverage verifies the approved bio content and existing About-page behavior.
- [x] `python manage.py check`, the full test suite, Black, and flake8 pass.
- [x] Browser validation confirms the updated bio is readable at mobile and desktop widths.

## Implementation notes

- Update the existing bio paragraph in `blog/templates/blog/about.html`.
- Extend `tests/test_blog.py` with an assertion for the approved text.
- Do not alter backend behavior or unrelated public-page content.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused automated and browser validation pass.
- The ticket is moved from `.tasks/todo/` to `.tasks/in-progress/` only when implementation begins, then to `.tasks/done/` after validation.
