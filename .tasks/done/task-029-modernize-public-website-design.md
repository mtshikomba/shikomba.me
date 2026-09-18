# task-029: Modernize the public website design

## User story

As a visitor to `shikomba.me`, I want the website to look modern, polished, and intentional so that I can quickly understand the owner's work and enjoy browsing the blog, projects, research, resume, and About pages.

## Problem

The site has a functional shared stylesheet, but the current public UI remains visually plain: the navigation, page introductions, content cards, metadata, calls to action, and footer have limited hierarchy and personality. The pages do not yet feel like one cohesive personal brand experience.

## Scope

Perform a visual design pass on the public-facing website while preserving all existing backend behavior and public routes.

### In scope

- Establish a distinctive but professional visual direction for the public site: expressive heading treatment, restrained color system, layered surfaces, clear spacing rhythm, and purposeful visual hierarchy.
- Redesign the shared shell: brand/wordmark treatment, navigation, active/hover/focus states, page background, content container, and footer.
- Improve the home/blog landing page with a stronger introduction, clear primary actions to Projects and Resume, and a more deliberate post-list presentation.
- Improve post detail readability with an editorial reading measure, metadata treatment, and clear return/navigation affordance.
- Improve Projects and Research pages with stronger scanning patterns, status/metadata hierarchy, and visually consistent cards or list rows.
- Improve Resume and About pages with clearer section grouping and prominent but restrained actions/contact links.
- Add a small set of meaningful page-load or reveal transitions that respect `prefers-reduced-motion`; avoid decorative animation that harms readability.
- Use local/static assets only where needed; the core experience must remain usable without external image/font requests.
- Preserve the existing responsive and accessibility requirements at 375px, 1440px, and 200% zoom.

### Out of scope

- Django models, migrations, views, URL names, admin UI, authentication, or content-management behavior.
- New product features such as comments, search, newsletter signup, contact forms, or project/research detail routes.
- Changing the owner's content, claims, email address, LinkedIn URL, publication URLs, or resume data.
- A marketing landing page unrelated to the existing blog/portfolio experience.

## UX specification

### Visual direction

Create a calm editorial portfolio for a software engineer and researcher: warm paper background, deep ink text, one confident accent color, strong typographic hierarchy, and compact utility details. The design should feel authored and contemporary without becoming a dashboard or a card grid template.

### Visual tokens

| Token | Value | Use |
| --- | --- | --- |
| `--ink` | `#1F2937` | Body text and headings |
| `--paper` | `#F7F4EE` | Page background |
| `--surface` | `#FFFDF9` | Content surfaces |
| `--line` | `#D9D4CA` | Borders and dividers |
| `--brand` | `#B45309` | Primary actions and active states |
| `--brand-dark` | `#92400E` | Hover and pressed states |
| `--muted` | `#5B6470` | Secondary metadata |
| `--success` | `#166534` | Ongoing/positive status only |

The implementation must verify normal text contrast at 4.5:1 or better and large text/controls at 3:1 or better. These values may be adjusted only when needed to meet those ratios.

### Typography

- Headings: `Georgia, "Times New Roman", serif` as the local-safe display stack.
- Body and interface text: `-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.
- Do not load fonts from a remote provider or make the layout depend on a network font request.

### Design constraints

- Use a small tokenized palette with a light background, high-contrast ink, one primary accent, and semantic status colors only where needed.
- Use a distinctive display face available through a robust local/system fallback stack for headings, paired with a highly readable sans-serif body stack. Do not make the site depend on a remote font provider.
- Keep card radius restrained at 8px or less. Avoid nested cards, excessive pills, decorative blobs, purple gradients, and generic hero copy.
- Use text or icon-plus-text for meaningful actions; do not hide primary navigation or actions behind unfamiliar icons.
- Maintain readable line lengths, visible focus rings, sufficient contrast, and clear touch targets.
- Motion must be subtle, short, and disabled or reduced when `prefers-reduced-motion: reduce` is active.
- Content must remain visible and usable when animation is unavailable or disabled.

## Acceptance criteria

- [x] Public pages share one coherent modern visual system implemented through the shared static stylesheet; no inline page-specific style blocks are introduced.
- [x] The shared shell has a recognizable brand treatment, responsive navigation, visible active state, visible keyboard focus, and a useful footer.
- [x] Home/blog, post detail, Projects, Research, Resume, and About pages each have a clear primary hierarchy and visually distinct page-level treatment while remaining part of the same system.
- [x] Home/blog presents the owner introduction and primary Projects/Resume actions before the post list, using the existing `projects:project-list` and `resume:resume-detail` routes and without inventing unsupported claims.
- [x] Post detail uses a comfortable reading measure, clear publication metadata, and an obvious route back to the blog list.
- [x] Projects and Research entries are scannable: title, status/date metadata, summary, tags or publication link, and external actions are visually separated and remain accessible.
- [x] Resume and About pages group content into readable sections; email, LinkedIn, and resume download actions remain prominent and usable.
- [x] Any entrance or hover motion respects `prefers-reduced-motion`, is disabled under `reduce`, and does not delay access to content or controls; content remains visible without animation.
- [x] At 375px, 1440px, and 200% browser zoom, public pages have no horizontal scrolling, clipped text, overlapping content, or unusable controls.
- [x] Public pages meet WCAG AA contrast expectations, retain logical heading order, and expose meaningful link/action names to assistive technology.
- [x] Existing automated tests and route behavior continue to pass without changes to backend assertions or URL names.
- [x] Browser validation covers home/blog, post detail, Projects, Research, Resume, and About at mobile and desktop widths, including keyboard focus, reduced-motion behavior, and 200% zoom.
- [x] Browser validation covers both empty and populated states for posts, projects, research, and resume content.
- [x] The footer contains only working links to existing site sections or confirmed contact destinations; no placeholder `#` or empty links are introduced.
- [x] Django admin remains unchanged.

## Implementation notes

- Build on `static/css/site.css` and the existing template block structure; keep `title`, `meta_description`, and `content` blocks intact.
- Prefer small template class/markup adjustments over duplicating styles across page templates.
- Use only existing content and routes unless a template needs a return link to an existing route.
- Run `python manage.py check`, `python manage.py test tests`, Black, and flake8 after implementation.
- Do not commit generated media, database files, or user-uploaded resume assets.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused browser checks and the full test suite pass.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
