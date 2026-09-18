# task-037: Balance Resume download spacing

## User story

As a visitor viewing the Resume page, I want the Download resume button to have even, intentional spacing above and below it so the page feels balanced and the button clearly belongs to the resume content.

## Problem

The Download resume link is wrapped in a plain paragraph with default margins, while the following `.resume-section` adds its own top padding and border. This creates visibly uneven vertical space around the button. The existing `.resume-download` CSS rule is not applied by the template.

## Scope

Adjust the Resume page's download-button wrapper and related spacing so the vertical rhythm above and below the button is consistent.

### In scope

- Apply the existing or revised `.resume-download` class to the correct button wrapper.
- Define intentional spacing above and below the Download resume button.
- Preserve the button's label, download route, icon, styling, focus state, and surrounding resume sections.
- Keep spacing responsive and consistent at mobile and desktop widths.
- Add focused regression coverage for the wrapper/class and rendered download control where practical.

### Out of scope

- Redesigning the Resume page or changing typography/content.
- Changing resume model fields, views, URLs, admin behavior, or migrations.
- Changing the spacing of unrelated buttons or sections.

## Acceptance criteria

- [x] The Download resume button has equal or intentionally balanced vertical spacing above and below it.
- [x] The button wrapper uses a dedicated, active class rather than relying on default paragraph margins.
- [x] The existing `.resume-download` rule is applied and corrected to define the active wrapper spacing.
- [x] The button remains linked to the resume download route and retains its label, icon, hover state, and visible focus state.
- [x] The first resume section does not appear redundantly detached from the button because of combined default margins and section padding.
- [x] At 375px and 1440px, the button and surrounding sections have no overlap, clipping, or horizontal scrolling.
- [x] Existing Resume content, empty state, navigation, accessibility, and reduced-motion behavior remain unchanged.
- [x] Focused automated coverage verifies the download control and spacing wrapper structure.
- [x] `python manage.py check`, the full test suite, Black, and flake8 pass.
- [x] Browser validation confirms balanced spacing at mobile and desktop widths.

## UX review

### Findings

- The current template wraps the button in an unclassified `<p>`, so browser default paragraph margins control part of the spacing.
- `.resume-download { margin-bottom: 2rem; }` exists in the stylesheet but is not used by the template.
- The following `.resume-section` adds `1.5rem` top padding and a top border, making the space below the button visually different from the space above it.

### UX acceptance criteria

- [x] The button's relationship to the intro and first section is visually clear at mobile and desktop widths.
- [x] The button remains comfortably usable by keyboard and touch users, with the existing focus indicator and target size preserved.
- [x] Spacing remains stable at 200% zoom without pushing content off-screen or creating unexpected gaps.

### UX review findings

- At both 375px and 1440px viewport checks, the measured gap from the intro to the button is approximately `48px`, while the gap from the button to the first resume section is approximately `16px`.
- The button itself is approximately `51px` tall and does not cause horizontal overflow, so its dimensions and focus target do not need redesigning.
- The current imbalance comes from the wrapper's default paragraph margins combined with the first `.resume-section` padding and border.
- The implementation should establish one deliberate spacing rhythm around the download action and avoid relying on browser-default paragraph margins.

### Additional UX acceptance criteria

- [x] The measured vertical gaps above and below the button are equal or intentionally documented as distinct, with no accidental `48px` versus `16px` mismatch.
- [x] The first section border begins at a visually deliberate distance from the button and does not make the button appear detached from the resume content.
- [x] The button remains at least `44px` tall and retains a visible focus indicator at all tested widths and zoom levels.
- [x] The empty Resume state is unaffected when no Resume record exists.

### Validation results

- Added `resume-download` wrapper coverage to `tests/test_resume.py`.
- The rendered gap from the intro to the button is `48px`, and the gap from the button to the first section is also `48px` at 375px and 1440px.
- The button remains `51px` tall with no horizontal overflow.
- Full validation passed: 34 tests, Django check, Black, flake8, and whitespace checks.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused automated and browser validation pass.
- The ticket is moved from `.tasks/todo/` to `.tasks/in-progress/` only when implementation begins, then to `.tasks/done/` after validation.
