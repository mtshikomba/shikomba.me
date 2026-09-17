# task-030: Add owner profile image to the About page

## User story

As a visitor to `shikomba.me`, I want to see a professional profile image of the owner on the About page so that the site feels personal and I can connect the written bio with the person behind the work.

## Problem

The About page currently introduces the site owner through text and contact links but has no visual identity for the person behind the blog, projects, research, and resume.

## Scope

Add the supplied owner profile image to the public About page as a local, accessible, responsive content asset.

### In scope

- Add the supplied profile image to a versioned public static/media asset location using a web-appropriate filename and format.
- Display the image on the About page alongside the existing owner introduction and contact links.
- Provide meaningful alternative text that identifies the image as the owner's profile portrait; do not rely on surrounding text alone.
- Use the existing public design system: restrained editorial framing, no decorative nested card, and a stable aspect ratio to avoid layout shift.
- Make the image responsive at 375px, 1440px, and 200% browser zoom without clipping important facial content, causing horizontal scrolling, or breaking adjacent text/actions.
- Preserve the existing About route, email/LinkedIn links, navigation, backend behavior, and admin interface.

### Out of scope

- Face recognition, image processing pipelines, user uploads, or admin-managed image editing.
- Adding profile images to the resume, blog posts, projects, or research entries.
- Changing the owner's bio, contact details, models, views, or URL names.
- External image hosting or remote image/font dependencies.

## Acceptance criteria

- [x] The supplied profile image is stored locally in a tracked public asset location and is referenced through Django's static asset handling.
- [x] The About page displays the profile image next to the owner's introduction and existing contact links.
- [x] The image has meaningful alt text, specifically `Portrait of Tangeni Shikomba`, and is not marked decorative.
- [x] The square supplied image uses a stable 1:1 responsive aspect ratio and preserves the full portrait without unnecessary cropping.
- [x] On desktop the image and About content can sit side by side; on mobile the image stacks above the text and contact actions.
- [x] At 375px, 1440px, and 200% browser zoom, the About page has no horizontal scrolling, clipped text, overlapping content, or unusable links.
- [x] Existing email and LinkedIn links remain present and functional.
- [x] Focused automated tests verify the About page renders the image source and meaningful alt text; existing tests continue to pass.
- [x] `python manage.py check`, Black, and flake8 pass.
- [x] Browser validation confirms the actual image resource loads successfully and the About layout remains usable at mobile and desktop widths.

## Implementation notes

- Recommended placement: the public About page, where the portrait supports the owner's introduction without competing with the homepage's primary writing/projects actions.
- Use `{% load static %}` and `{% static %}` in the About template; do not hardcode an absolute filesystem or deployment URL.
- Use a 1:1 image frame matching the supplied square asset. Prefer rendering the full image without cropping; if `object-fit` is needed, verify that the face and clothing remain fully visible.
- Use the responsive layout sequence: image beside the About content at desktop widths, image first and content below at mobile widths.
- Use `alt="Portrait of Tangeni Shikomba"`; do not use an empty alt attribute or rely only on a caption.
- Keep the image asset reasonably sized for web delivery and do not commit generated media or private uploads.
- Follow repository conventions and avoid backend changes for this presentation-only feature.

## Definition of done

- Acceptance criteria are met and documented in the pull request.
- Focused and full test suites pass.
- Browser validation covers the About page at mobile, desktop, and 200% zoom.
- The ticket is moved from `.tasks/todo/` to `.tasks/done/` only after implementation and validation are complete.
