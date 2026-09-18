# task-036: Refresh branding and contact links

## User story

As a visitor to shikomba.me, I want the site favicon, displayed name, footer navigation, and contact links to reflect the owner's current brand and provide recognizable, accessible ways to reach the owner.

## Problem

The shared site shell does not declare a favicon, the blog homepage still refers to Tangeni Shikomba, the footer duplicates the About route, and About/footer contact links are presented as text-only links rather than recognizable icons.

## Scope

Update the public branding and contact-link presentation using the existing brand logo and current public identity.

### In scope

- Add a favicon based on the existing `tangeni-shikomba-brand.jpg` brand logo.
- Replace the blog homepage's visible “Tangeni Shikomba” reference with “Matheus T. Shikomba”.
- Remove the About link from the footer while preserving the footer's contact destinations.
- Replace the About-page and footer Email, LinkedIn, and GitHub text links with relevant recognizable icons.
- Keep every contact destination functional and provide accessible names for icon-only links.
- Preserve the existing header navigation, About-page bio, profile image, layout, routes, and brand image treatment.

### Out of scope

- Changing the About-page bio content.
- Redesigning the broader visual system or changing unrelated page copy.
- Removing the header About navigation link.
- Changing Django models, views, URLs, admin behavior, or migrations.
- Adding third-party tracking or remote icon assets without an explicit dependency decision.

## Acceptance criteria

- [x] The shared document head declares a favicon using the existing brand logo asset, and the favicon loads successfully.
- [x] The blog homepage displays “Matheus T. Shikomba” wherever the current blog hero refers to Tangeni Shikomba.
- [x] The footer no longer renders an About link, while Email, LinkedIn, and GitHub destinations remain available.
- [x] About-page contact links use recognizable Email, LinkedIn, and GitHub icons instead of text-only labels.
- [x] Footer contact links use the same relevant icons consistently.
- [x] Every icon-only link has an accessible name through visible text, an accessible label, or an equivalent semantic treatment; decorative icon elements are hidden from assistive technology.
- [x] Email, LinkedIn, and GitHub URLs remain unchanged and functional.
- [x] The header About link, About-page bio, profile image, brand logo, and all existing routes remain unchanged.
- [x] At 375px and 1440px, icon links and footer content remain visible, identifiable, keyboard accessible, and free of clipping or horizontal scrolling. A 720px CSS viewport was also checked as the 200% zoom equivalent; the integrated browser did not expose a direct zoom control.
- [x] Focus-visible styles remain clear on all icon links and keyboard navigation order remains logical.
- [x] Focused automated tests cover favicon markup, the updated homepage identity, footer link removal, preserved destinations, and accessible icon labels.
- [x] `python manage.py check`, the full test suite, Black, and flake8 pass.
- [x] Browser validation confirms the favicon, identity text, footer structure, icon links, responsive layout, and keyboard focus states.

## Implementation notes

- The existing logo is `static/images/tangeni-shikomba-brand.jpg`; assess whether the browser accepts it directly as a favicon or whether a derived local favicon asset is needed.
- The repository currently has no visible icon dependency. Prefer an existing local pattern or a small accessible implementation over introducing an unnecessary dependency.
- Keep visible labels or tooltips where needed so unfamiliar icons remain understandable without relying on color or shape alone.
- Update `tests/test_blog.py` or another focused public-shell test module; do not alter backend behavior.

## UX review

### Findings

- The current shared shell has no favicon declaration, so browser tabs do not expose the existing brand mark.
- The blog hero still names Tangeni Shikomba while the About bio and footer use Matheus T. Shikomba, creating an inconsistent public identity.
- The footer repeats the About destination already present in primary navigation.
- About and footer contact links currently rely on visible text labels and do not provide a compact, recognizable contact-link treatment.
- Replacing text with icons creates an accessibility and discoverability risk unless each icon has an accessible name, a tooltip/title, a clear focus state, and sufficient touch target size.

### UX acceptance criteria

- [ ] The favicon uses the same brand mark shown in the header and remains legible at browser-tab size.
- [ ] About-page and footer contact icons use consistent visual styling, alignment, and minimum hit areas across desktop and mobile.
- [ ] Each contact icon communicates its destination through an accessible name and a visible tooltip or equivalent hover/focus description; meaning must not depend on color alone.
- [ ] Keyboard users can reach the contact icons in a logical order and see a clear `:focus-visible` indicator.
- [ ] On mobile, the footer icons wrap or stack without crowding, clipping, or reducing the touch target below an ergonomic size.
- [ ] Removing the footer About link does not remove access to About from the primary navigation.
- [x] Browser review covers favicon presence, homepage identity, About contact links, footer contact links, hover/focus states, 375px, 1440px, and a 720px CSS viewport equivalent to 200% zoom.

### Validation results

- The favicon resolved to `/static/images/tangeni-shikomba-brand.jpg`.
- Homepage identity rendered as “Matheus T. Shikomba”; the old “Tangeni Shikomba” text was absent.
- Footer About was absent while the header About link remained available.
- About and footer rendered Email, LinkedIn, and GitHub icons with accessible labels and 44px by 44px hit areas.
- Keyboard focus remained visible and both mobile and desktop layouts had no horizontal overflow.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused automated and browser validation pass at mobile, desktop, and zoomed layouts.
- The ticket is moved from `.tasks/todo/` to `.tasks/in-progress/` only when implementation begins, then to `.tasks/done/` after validation.
