# task-031: Add brand image to the public site shell

## User story

As a visitor to `shikomba.me`, I want the site to use the owner's brand image consistently so that the website has a recognizable visual identity across its public pages.

## Problem

The public shell currently uses a generated circular `S` mark and text-only footer branding. It does not use the supplied brand image/logo.

## Scope

Add the supplied brand image as a locally served brand asset and use it in the shared public header and footer.

### In scope

- Add the supplied brand image to a tracked public static asset location using a web-appropriate filename and format.
- Replace the generated `S` header mark with the supplied brand image while retaining a readable `shikomba.me` wordmark.
- Optionally add a smaller version of the supplied brand image to the footer brand treatment only if it does not create repetitive branding or compete with footer links.
- Reference the asset through Django's `{% static %}` handling; do not hardcode deployment paths or use external hosting.
- Preserve existing navigation, route behavior, contact links, content, backend behavior, and admin UI.
- Add focused template coverage for the asset source and accessible brand treatment.

### Out of scope

- Redesigning the full public site beyond the shared brand treatment.
- Changing the supplied image, generating alternate logos, or adding an image-processing pipeline.
- Adding user uploads, admin-managed branding, or a branding settings model.
- Changing the Django admin UI, models, views, URL names, or content.
- Adding a favicon/app icon unless the supplied asset is explicitly suitable and a separate requirement is confirmed.

## Acceptance criteria

- [x] The supplied brand image is stored locally in a tracked public asset location and served through Django static assets.
- [x] The public header uses the supplied brand image in the home/brand link and retains visible `shikomba.me` text.
- [x] The public footer retains readable branding and existing footer links remain available; a smaller footer image is used only when it improves the composition without unnecessary repetition.
- [x] The header image uses `alt=""` because the surrounding `aria-label="shikomba.me home"` and visible wordmark provide the accessible name; any standalone informative use has meaningful alt text.
- [x] Header and footer branding have stable dimensions and remain legible at 375px, 1440px, and 200% browser zoom without horizontal scrolling or layout shift.
- [x] The brand image is presented as a clean circular mark without distortion, filters, overlays, or background treatment that reduces contrast; the source asset remains unchanged.
- [x] The header image has a mobile size cap so it does not force awkward navigation wrapping.
- [x] If the image request fails, the visible `shikomba.me` wordmark still identifies the site and the layout remains stable.
- [x] Focused automated tests verify the static image reference and existing navigation/footer destinations continue to render.
- [x] `python manage.py check`, the full test suite, Black, and flake8 pass.
- [x] Browser validation confirms the actual image resource loads and the header/footer remain usable at mobile and desktop widths.

## Implementation notes

- Recommended placement: shared `templates/base.html`, primarily in the existing `.site-brand` header link. A smaller footer image is optional and should be omitted if it makes the shell feel repetitive.
- Use `{% load static %}` and `{% static %}`; do not use a hardcoded absolute URL.
- Preserve the visible text wordmark alongside the image for recognition and resilience if the image fails to load.
- Use `alt=""` for the header image because the labeled brand link already names the destination; use meaningful alt text only when the image is independently informative.
- Use explicit width/height or an equivalent stable CSS sizing strategy to prevent layout shift; keep the image responsive and use a circular frame without modifying the source asset.
- Do not add CSS filters, overlays, gradients, or decorative backgrounds to the supplied image.
- Keep the implementation presentation-only and build on `static/css/site.css`.
- Do not commit generated media or private uploads.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused and full test suites pass.
- Browser validation covers the public header and footer at mobile, desktop, and 200% zoom.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
