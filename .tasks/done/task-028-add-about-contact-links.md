# task-028: Add contact links to the About page

## User story

As a visitor to `shikomba.me`, I want to find the owner's email address and LinkedIn profile on the About page so that I can contact them or learn more about their professional background.

## Problem

The public About page currently contains only placeholder introduction text and does not provide the owner's requested contact or professional profile links.

## Scope

Update the public About page to show the owner's email address and LinkedIn profile.

### In scope

- Display `tangenishikomba@gmail.com` as a working `mailto:` link with accessible link text.
- Display a working LinkedIn link to `https://www.linkedin.com/in/tangeni-shikomba`.
- Keep the content within the existing About-page layout and shared public design system.
- Add focused template/view coverage for the visible email and LinkedIn destinations.
- Preserve existing routes, navigation, models, admin behavior, and other public pages.

### Out of scope

- Contact forms, email delivery, newsletter signup, or social integrations.
- Changing the owner bio beyond the requested contact/profile links.
- Updating the Django admin interface or adding new models/settings.

## Acceptance criteria

- [x] The About page displays `tangenishikomba@gmail.com` as a working `mailto:tangenishikomba@gmail.com` link.
- [x] The About page displays a LinkedIn link targeting `https://www.linkedin.com/in/tangeni-shikomba`.
- [x] Both links have descriptive, accessible visible text and remain usable by keyboard.
- [x] The existing About route continues to return a successful response and keeps exactly one `h1`.
- [x] The links fit within the responsive About-page layout at 375px and 1440px without horizontal scrolling or clipped text.
- [x] Focused automated tests verify the email and LinkedIn URLs are rendered.
- [x] Existing tests continue to pass, `python manage.py check` passes, and black/flake8 checks pass.

## Implementation notes

- Update `blog/templates/blog/about.html` only unless a focused test change is required.
- Use the existing `card` styling from `static/css/site.css`; do not introduce a second public styling system.
- Use `mailto:` for email. The LinkedIn URL may open in the same tab; if a new tab is chosen, include appropriate `rel` security attributes.
- Follow repository conventions: explicit type hints and Google-style docstrings for any new Python code.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused and full test suites pass.
- Browser validation covers the About page at mobile and desktop widths.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
