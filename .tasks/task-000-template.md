# task-001: Refresh public website UX/UI

## User story

As a prospective passenger, driver, business customer, or supplier, I want the Pamoja Fleet website to feel trustworthy, clear, and easy to use on any device so that I can quickly understand the offer and complete the right contact or partnership action.

## Problem

The public website is functional but has an inconsistent, Bootstrap-default presentation across its pages. The shared layout contains most styling as inline CSS, the footer includes placeholder legal and social links, several calls to action point to `#`, and some pages depend on remote imagery. The navigation and forms also need a responsive and accessibility pass.

## Scope

Update the public Django website in `yango_project/website/` while preserving existing URL names, form submissions, models, and backend behavior.

### In scope

- Establish a cohesive visual system in the shared website shell: typography, color tokens, spacing, buttons, cards, focus states, navigation, footer, and page sections.
- Improve the home page hierarchy so the primary value proposition and next actions are immediately clear.
- Make Services, Vision, Fleet, and Partner pages visually consistent with the home page while retaining their existing content and routes.
- Replace or remove dead `#` links and empty legal links. Every visible action must either navigate to an existing route, use a real contact/download destination supplied by the product owner, or be removed until a destination exists.
- Use available local assets where practical and provide robust image fallbacks/alt text. Do not make the site depend on third-party image hosts for its core experience.
- Improve forms on the driver, business, and supplier pages: clear labels, grouped fields where helpful, visible required/error states, preserved values after validation errors, success feedback, and usable controls on narrow screens.
- Make the shared navigation keyboard accessible, visibly indicate the current page, and ensure the mobile menu does not cause horizontal overflow.
- Add semantic structure and accessible names for icon-only or social controls. Maintain sufficient color contrast and visible keyboard focus.
- Add responsive layouts for desktop and mobile widths, including long headings, cards, buttons, forms, images, and footer columns.

### Out of scope

- Changing Django models, authentication, authorization, form fields, URL names, or submission behavior.
- Adding unsupported claims, real app-store URLs, social profiles, legal policy content, contact details, or business metrics without product confirmation.
- Redesigning the authenticated fleet portal.

## Acceptance criteria

1. All existing public routes continue to return successful responses: `/`, `/services/`, `/vision/`, `/fleet/`, `/partner/drivers/`, `/partner/business/`, and `/partner/suppliers/`.
2. The public pages share one coherent visual language and no longer rely on scattered page-specific inline styling for common components.
3. The primary action on each page is visually distinct and has a valid destination or submits the relevant existing form.
4. No user-facing link uses a placeholder `#` or empty `href`. Unsupported destinations are represented by intentional non-link content or are omitted.
5. Navigation works with keyboard and touch, includes a visible focus state, exposes the mobile menu accessibly, and identifies the current page.
6. Forms retain server-side Django validation and CSRF protection. Invalid submissions visibly associate errors with their fields; valid submissions show the existing success message and redirect behavior.
7. Images have meaningful alt text, are locally available for the core experience where an equivalent asset exists, and do not distort or cause layout shift in the page layout.
8. At viewport widths of 375px and 1440px, pages have no horizontal scrolling, no overlapping content, no clipped text, and controls remain usable.
9. Body text and controls meet a readable contrast target, keyboard focus is visible, heading order is logical, and icon-only controls have accessible labels.
10. The implementation adds or updates focused website tests for route rendering, key navigation/CTA destinations, and successful/invalid form states where testable server-side.
11. Browser validation is performed at mobile and desktop widths for the home page plus one content page and one form page, checking loading, navigation, focus, validation errors, success feedback, and overflow.
12. The implemented UI uses the approved warm palette: charcoal/cream structure, terracotta primary actions, amber emphasis, and sage only for semantic success; no unintended Bootstrap blue or green remains in shared public-site components.
13. The implemented UI uses Fraunces or the documented display fallback for headings and DM Sans or the documented body fallback for interface text, with no layout shift or overflow when fonts are unavailable.
14. Primary and secondary controls meet the documented color-contrast ratios in default, hover, pressed, disabled, and focus-visible states.
15. The palette and typography remain legible and visually coherent at 375px, 1440px, and 200% browser zoom; no heading, button label, navigation item, or form label is clipped.

## UX acceptance criteria

- A first-time visitor can identify what Pamoja Fleet does and choose Passenger, Business, Driver, or Supplier actions without reading the entire page.
- The visual hierarchy remains understandable with browser zoom at 200%.
- Interactive elements have a clear hover/focus/pressed state and touch targets are comfortably usable.
- Form errors appear near the relevant field and do not disappear behind the sticky/mobile navigation or footer.
- Success feedback is prominent, understandable, and announced appropriately for assistive technology.
- The footer is useful rather than decorative: contact methods and navigation links work, and unavailable legal/social destinations are not presented as active links.
- The first viewport feels warm, capable, and locally grounded rather than blue/green, with terracotta reserved for actions and charcoal providing visual stability.
- Headings are recognizably editorial and distinctive; body copy remains quiet, readable, and easy to scan.
- Color communicates hierarchy and state without requiring the visitor to interpret a new brand color on every section.

## UX specification

### Experience principles

- **Clear first:** Each page communicates one primary job and presents one dominant next action before secondary actions.
- **Trust through evidence:** Use real fleet imagery, maintenance details, safety language, and locally relevant copy without inventing claims or metrics.
- **Warm and operational:** The visual tone should feel capable and human, with strong contrast, restrained decoration, and clear information grouping.
- **Progressive detail:** Lead with scannable headings and short summaries; expose supporting detail through lists, feature blocks, and focused sections.
- **Respect the user state:** Preserve entered form values after validation errors, explain what needs attention, and confirm successful submission without requiring a second submission.

### Visual direction

Replace the current Bootstrap-blue and green combination with a warm, grounded logistics identity. The design should feel dependable and human without looking like a generic corporate dashboard or a transportation app template.

#### Color system

| Token | Value | Use |
| --- | --- | --- |
| `--ink` | `#242628` | Body text, dark navigation, footer, strong headings |
| `--brand` | `#A8473A` | Primary buttons, active links, key headings, brand accents |
| `--brand-dark` | `#79332E` | Hover/pressed states and dark brand surfaces |
| `--paper` | `#FBF8F2` | Main page background |
| `--surface` | `#FFFDF9` | Cards, forms, and content panels |
| `--line` | `#E3D8CC` | Borders and dividers |
| `--accent` | `#E6A63A` | Small highlights, focus-adjacent emphasis, brand detail; never use for long body text |
| `--success` | `#3F705D` | Success messaging and positive status only |
| `--muted` | `#65706D` | Secondary text that still meets contrast requirements |

Color rules:

- Use charcoal and cream as the structural pair; terracotta is the single primary action color.
- Use amber sparingly as a visual signal, not as a paragraph or small-label color on a light background.
- Use sage only for semantic success or verified positive states; do not create a second green brand identity.
- Override Bootstrap `bg-primary`, `text-primary`, button, link, and focus treatments so the legacy blue does not reappear in shared components.
- Do not use a blue/green gradient. If a hero image needs treatment, use a solid charcoal overlay with a subtle terracotta edge or no overlay where text contrast permits.
- Every text/background pairing must meet WCAG AA contrast: 4.5:1 for normal text and 3:1 for large text and graphical controls.

#### Typography

- Use **Fraunces** for the brand wordmark, page titles, hero headings, and section headings. It gives the site a distinctive editorial voice without sacrificing seriousness.
- Use **DM Sans** for body text, navigation, labels, buttons, metadata, and form controls. It remains highly legible at mobile sizes.
- Load the fonts with a robust fallback stack: `Georgia, serif` for display text and `"Trebuchet MS", sans-serif` for body text if the hosted font is unavailable.
- Body text starts at `1rem` with a line height of at least `1.55`; supporting text must not drop below `0.875rem`.
- Page titles use responsive sizing with a clamp range, but no text may overflow at 375px or 200% zoom.
- Use `font-weight: 700` for headings and primary actions, `600` for labels and navigation, and regular weight for long-form copy.
- Keep letter spacing at normal (`0`); reserve uppercase styling for short kickers and never for paragraphs or long navigation labels.

#### Component styling

- Use small, restrained radii between `4px` and `8px`; avoid pill-shaped cards and decorative nested cards.
- Use one shadow family with low opacity for raised forms and repeated content blocks; page sections remain unframed.
- Primary buttons use terracotta with white text; hover and pressed states use `--brand-dark`.
- Secondary buttons use transparent cream/surface backgrounds with a terracotta border and text.
- Focus rings use a 3px amber outline with visible offset and must remain visible against dark and light surfaces.
- Icons support meaning but never replace the visible action label for core navigation or form actions.
- Use local fleet imagery as content evidence. Images must have stable aspect ratios and must not be used as dark decorative texture when the visitor needs to inspect the vehicle.

### Primary user flows

1. **Passenger:** Home or Services -> understand ride-hailing offer -> Services/Yango app action or contact route.
2. **Business customer:** Home or Services -> Business Solutions -> review service options -> submit business quote form -> see success confirmation.
3. **Driver applicant:** Home or navigation -> Drive With Us -> scan partnership benefits -> submit driver application -> see success confirmation.
4. **Supplier:** Navigation/footer -> Supplier Partners -> review partnership fit -> submit supplier interest form -> see success confirmation.
5. **Fleet/brand researcher:** Home -> Fleet or Vision -> review proof points -> choose a relevant partnership or service action.

### Page specifications

| Surface | Required hierarchy and behavior |
| --- | --- |
| Shared shell | Header presents the Pamoja Fleet identity, primary links, and a clearly labeled partnership menu. Current page is visually and programmatically identifiable. Footer groups navigation, partnerships, and verified contact details; unavailable legal/social destinations are omitted or rendered as plain text. |
| Home | Hero states what the company does in Namibia and offers clear paths for passengers, businesses, and drivers. Follow with proof points, fleet/driver credibility, and a final action band. The first viewport must expose the headline and at least one meaningful next action without relying on a card-only hero. |
| Services | Separate passenger and business needs visually. Passenger section leads to the actual available ride action; business section leads to the quote form. Service benefits are scannable and repeated calls to action are not competing with one another. |
| Vision | Present mission, values, and strategic focus as a readable narrative. End with driver and business partnership actions. Avoid making every content block look like a separate floating card. |
| Fleet | Lead with vehicle quality, maintenance, and safety. Use stable image ratios and concise feature groups. Fleet claims and statistics remain unchanged unless verified by the product owner. |
| Partner pages | Use a two-column layout on wide screens and a single-column sequence on small screens: audience benefit summary first, form second. Keep the form heading and submit action visible in the same context as the supporting copy. |

### Form states

- **Initial:** Group related fields, show visible labels and required status, use appropriate input types, and provide concise examples through placeholders or help text.
- **Focused:** Show a high-contrast focus indicator that is not conveyed by color alone.
- **Invalid:** Keep all submitted values, place the field error next to its field, connect the error with `aria-describedby`/`aria-invalid` where applicable, and provide a summary or page-level cue for the first invalid field.
- **Submission:** Prevent accidental duplicate submission feedback through a clear pending state if client-side enhancement is added; do not alter the existing server-side POST behavior.
- **Success:** Preserve the existing redirect and Django message behavior, place the confirmation near the top of the page, use an appropriate status/live-region pattern, and make the next expected action clear.
- **Server/unexpected error:** Keep the form usable and show a plain-language recovery message without exposing stack traces or internal details.

### Responsive and accessibility behavior

- At 375px wide, content uses the full available width with safe side padding; no section, table-like metric row, form control, button label, or navigation item is clipped.
- At 1440px wide, reading measure stays comfortable and content does not stretch into long, difficult-to-scan lines.
- At 200% zoom, the layout may reflow but must remain usable without horizontal scrolling for normal page content.
- The mobile menu is operable by keyboard and touch, exposes its expanded/collapsed state, and returns focus predictably when closed.
- Keyboard users can reach every action in logical order, see a persistent focus ring, and skip repetitive navigation where appropriate.
- Heading levels follow document structure (`h1` once per page, then ordered subsections); decorative icons are hidden from assistive technology and informative icons have an accessible name.
- Text and controls meet WCAG AA contrast expectations; color is never the only indicator of state.
- Images have concise, contextual alt text; decorative images use empty alt text. Core content does not fail when remote image requests are unavailable.

### Content and interaction rules

- Use action labels that describe the outcome, such as `Request a business quote`, `Apply to drive`, and `Register supplier interest`.
- Do not present placeholder app-store, social, legal, or contact links as functional controls. Use confirmed destinations only.
- Keep the existing contact details and performance claims until they are verified; do not add new claims during the visual refresh.
- Do not hide important form requirements in hover-only UI or rely on placeholder text as the field label.

### UX validation checklist

- Test the home page, Services page, and one partner form at 375px and 1440px.
- Navigate the header, primary CTA, form, and footer using keyboard only.
- Verify collapsed and expanded mobile navigation, focus visibility, and no horizontal overflow.
- Submit each form once with missing/invalid required values and verify inline errors and retained values.
- Submit each form with valid fixture data and verify the success message and redirect.
- Test browser zoom at 200% and confirm headings, buttons, form errors, and footer content remain readable.
- Disable remote image loading or simulate a failed image request and verify the page still communicates its purpose.

## Implementation notes

- Start with `yango_project/website/templates/website/base.html` and introduce a dedicated website stylesheet under the app's static files for shared styles.
- Reuse the existing Bootstrap dependency and Bootstrap Icons where it reduces risk, but do not let default Bootstrap styling determine the entire visual identity.
- Keep Django template URL names unchanged.
- Prefer existing local assets in `yango_project/website/static/website/`; coordinate any new asset requirements before adding them.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused Django tests pass, `python manage.py check` passes, and no migrations are generated because this is a presentation-only change.
- Desktop/mobile browser validation is recorded, including the tested viewport sizes and any known limitations.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
