# task-034: Standardize public typography

## User story

As a visitor, I want headings and supporting text to use a consistent type scale and font treatment across each page so the site feels cohesive and the resume introduction is easy to read.

## Problem

The resume intro uses a split layout where the text below the `h1` is styled separately through `.page-intro--split > p`. It appears visually inconsistent with equivalent introductory text on the Projects, Research, and About pages.

## Scope

Standardize the public page typography while preserving the existing editorial heading/body hierarchy.

### In scope

- Define and apply consistent font family, size, weight, and line-height rules for page `h1` headings, page-intro supporting text, section `h2` headings, and body content.
- Make the resume text below the `h1` visually match equivalent page-intro text on Projects, Research, and About.
- Make the blog hero supporting text match the shared page-intro supporting-text scale.
- Prefer shared typography selectors or tokens over page-specific overrides.
- Preserve existing wording, routes, navigation, resume content, and download behavior.
- Add focused regression coverage for the shared typography selectors or rendered page structure.

### Out of scope

- Changing the site content, information architecture, or navigation.
- Changing Django models, views, URLs, admin behavior, or migrations.
- Replacing the existing editorial font direction with a new visual design system.

## Acceptance criteria

- [x] Public `h1`, `h2`, page-intro supporting text, and body content use an intentional, documented-in-code type scale and font treatment.
- [x] Resume supporting text below the `h1` matches equivalent page-intro text on Projects, Research, and About at desktop and mobile widths.
- [x] Blog hero supporting text uses the shared `1.1rem` supporting-text size instead of a larger responsive size.
- [x] Existing heading/body hierarchy remains readable and consistent across the public pages.
- [x] No page-specific typography override is introduced unless required by layout and covered by a focused test.
- [x] At 375px and 1440px, affected pages have no clipped text, overlap, unusable controls, or horizontal scrolling. Browser zoom remains a manual follow-up because the integrated browser did not expose a working zoom control.
- [x] Existing routes, resume content, download behavior, accessibility, and reduced-motion behavior remain unchanged.
- [x] Focused automated coverage is added or updated for the typography behavior.
- [x] `python manage.py check`, the full test suite, Black, and flake8 pass.
- [x] Browser validation confirms consistent typography on the About, Projects, Research, and Resume pages.
- [x] Browser validation confirms the blog hero supporting text computes to `17.6px`, matching the other page intros, with no horizontal overflow.

## Implementation notes

- Start with the shared rules in `static/css/site.css`, especially the global heading rules and `.page-intro` selectors.
- Inspect the resume split-intro layout at mobile widths before changing its structure.
- Avoid changing content or backend behavior.

## UX review

### Findings

- About, Projects, Research, and Resume currently share the same heading family and supporting-text family, size, and line-height.
- The resume is visually different because `.page-intro--split` places its supporting paragraph in a separate grid column and bottom-aligns it beside the `h1`.
- At 375px, the resume intro stacks without horizontal overflow or clipping.
- At 1440px, the resume supporting paragraph begins substantially lower than equivalent introductory text on the other pages, which makes the intro feel misaligned rather than incorrectly sized.

### UX acceptance criteria

- [x] On desktop, the resume intro has a deliberate, readable relationship between the `h1` and supporting paragraph; the supporting paragraph is no longer accidentally vertically offset.
- [x] On mobile, the resume intro remains stacked, readable, and free of horizontal scrolling or clipped text.
- [x] The shared heading and supporting-text treatment remains visually consistent across About, Projects, Research, and Resume.
- [x] Keyboard focus indicators, skip navigation, link targets, readable contrast, and reduced-motion behavior remain unchanged.
- [x] Browser review covers 375px and 1440px viewports, including the resume download control and section headings.

### Follow-up update

The blog homepage hero copy was identified as a second typography outlier. Its `.hero__lede` rule used `clamp(1.05rem, 2vw, 1.25rem)`, which rendered at `20px` on desktop while the other page-intro supporting text rendered at `17.6px`. The rule now uses the shared `1.1rem` size, and `tests/test_blog.py` asserts that size remains present.

Validation after the follow-up:

- `python manage.py test tests` passed with 30 tests.
- Black and flake8 passed.
- Browser verification at the live homepage confirmed `17.6px / 29.04px` and no horizontal overflow.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused automated and browser validation pass.
- The ticket is moved from `.tasks/todo/` to `.tasks/in-progress/` only when implementation begins, then to `.tasks/done/` after validation.
