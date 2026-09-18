# task-032: Update public identity text and add GitHub links

## User story

As the site owner, I want the public website to use `Matheus T. Shikomba` as my displayed name, remove the visible `shikomba.me` wordmark text, and link to my GitHub profile so visitors see the correct identity and can find my code.

## Problem

The public shell and About page still display the old visible `shikomba.me` branding and `Tangeni Shikomba` name. The About page and footer also do not link to the owner's GitHub profile.

## Scope

Update visible public-facing identity text and add GitHub links without changing the site's domain, routes, backend behavior, or admin interface.

### In scope

- Remove visible `shikomba.me` wordmark text from the shared header and footer brand treatments while preserving the existing brand image and accessible home-link labeling.
- Replace visible `Tangeni Shikomba` owner-name text with `Matheus T. Shikomba` wherever it appears in public page content or the shared footer copyright.
- Update the public profile image alternative text from `Portrait of Tangeni Shikomba` to `Portrait of Matheus T. Shikomba`.
- Add a GitHub link to `https://github.com/mtshikomba` on the About page alongside the existing email and LinkedIn links.
- Add a GitHub link to the shared footer alongside the existing contact/profile links.
- Use descriptive visible link text (`GitHub profile`) and preserve keyboard focus/accessibility behavior.
- Preserve technical domain references such as the deployed host, URL paths, image filenames, and any required document metadata unless a separate domain-change request is made.

### Out of scope

- Changing the deployed domain from `shikomba.me`.
- Renaming image files, Django apps, URL names, models, migrations, settings, or admin content.
- Changing the supplied brand/profile images.
- Adding GitHub API integration, repository listings, authentication, or social embeds.
- Redesigning the public site beyond the requested identity/link updates.

## Acceptance criteria

- [x] The shared header no longer displays visible `shikomba.me` wordmark text; the brand image remains a working home link with an accessible name.
- [x] The shared footer no longer displays visible `shikomba.me` wordmark text and continues to provide working existing footer links.
- [x] The footer contains no brand image; the brand image appears only in the shared header.
- [x] The footer copyright is left-aligned while the footer links remain right-aligned on wide screens.
- [x] On smaller screens, the footer links remain right-aligned and the copyright is the final item at the bottom of the footer.
- [x] Public owner-name text is updated from `Tangeni Shikomba` to `Matheus T. Shikomba` wherever it is displayed by the shared shell or About page.
- [x] The profile image uses `alt="Portrait of Matheus T. Shikomba"` so assistive technology receives the updated identity.
- [x] The About page contains a visible `GitHub profile` link targeting `https://github.com/mtshikomba`.
- [x] The footer contains a visible `GitHub profile` link targeting `https://github.com/mtshikomba`.
- [x] Email and LinkedIn links remain present and unchanged.
- [x] The deployed domain and technical `shikomba.me` URL references remain unchanged.
- [x] Links have descriptive accessible text, visible keyboard focus, and no placeholder or empty destinations.
- [x] After removing the visible wordmark, the image-only portion of the home link remains accessible through its existing `aria-label="shikomba.me home"` and is not an unlabeled control.
- [x] At 375px, 1440px, and 200% browser zoom, header/footer identity and links remain readable without horizontal scrolling or overlap.
- [x] Focused automated tests verify the updated name, removal of visible wordmark text, GitHub URLs, and preservation of email/LinkedIn links.
- [x] `python manage.py check`, the full test suite, Black, and flake8 pass.

## Implementation notes

- Update `templates/base.html` for shared header/footer text and GitHub footer link.
- Remove the footer brand-image element and keep the footer as copyright plus navigation links with explicit responsive alignment.
- Update `blog/templates/blog/about.html` for the displayed owner name and GitHub link.
- Update the profile image alt text to `Portrait of Matheus T. Shikomba`; keep the existing image filename unchanged because it is a technical asset path.
- Keep the brand image and its accessible `aria-label` behavior intact.
- Test visible rendered content rather than asserting that all occurrences of the domain string disappear from HTML, because technical URLs and page metadata may still require `shikomba.me`.
- Follow repository conventions and do not change backend behavior for this presentation-only task.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused and full test suites pass.
- Browser validation covers the About page and shared shell at mobile, desktop, and 200% zoom.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
