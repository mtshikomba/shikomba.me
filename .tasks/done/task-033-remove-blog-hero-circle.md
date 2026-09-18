# task-033: Remove decorative blog hero circle

## User story

As a visitor to `shikomba.me`, I want the blog homepage to stay focused on the introduction and writing so that decorative elements do not distract from the content.

## Problem

The blog homepage currently renders a decorative circular element through the hero stylesheet pseudo-element. It has no functional meaning and is visually unnecessary.

## Scope

Remove the decorative circle from the public blog homepage while preserving the existing hero content, layout, branding, navigation, and responsive behavior.

### In scope

- Remove the `.hero::after` decorative circle from `static/css/site.css`.
- Preserve the homepage hero heading, intro copy, Projects/Resume actions, latest-writing section, and all existing routes.
- Confirm the hero remains visually balanced after the decorative element is removed.
- Preserve accessibility, responsive behavior, and reduced-motion behavior.

### Out of scope

- Removing the circular brand image/logo from the header.
- Changing the profile image or any content wording.
- Redesigning the homepage or changing the broader visual system.
- Changing Django models, views, URLs, admin behavior, or backend logic.

## Acceptance criteria

- [ ] The decorative `.hero::after` circle is removed from the public stylesheet.
- [ ] The homepage retains its hero heading, intro copy, Projects/Resume actions, and latest-writing content.
- [ ] The circular brand image in the shared header remains unchanged.
- [ ] At 375px, 1440px, and 200% browser zoom, the homepage has no horizontal scrolling, clipped text, overlap, or unusable controls.
- [ ] Existing automated tests continue to pass and no backend behavior changes.
- [ ] `python manage.py check`, Black, and flake8 pass.
- [ ] Browser validation confirms the decorative circle is absent and the hero remains balanced at mobile and desktop widths.

## Implementation notes

- This is a small follow-up to task-029; remove only the `.hero::after` rule and any styling that exists solely for that pseudo-element.
- Do not remove `.site-brand__mark` or other circular image treatments; those are functional brand/profile assets.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused browser checks and the full test suite pass.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
