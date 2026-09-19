# task-041: Create production docker-compose.yaml

## User story

As the developer deploying shikomba.me, I want a `docker-compose.yaml` that starts the Django service in a production environment using the image built by task-040, so the containerized deployment strategy from task-039 has a concrete, runnable Compose definition.

## Relationship to other tickets

This ticket implements the `web` service Compose deliverable that is part of task-039 Phase 1/2 ("Container and application readiness" / "Ubuntu Docker VM runtime"). It builds on the `Dockerfile` and `entrypoint.sh` created in task-040. It does not implement the MySQL service, reverse-proxy service, backups, or automatic deployment; those remain in task-038/task-039.

## Confirmed production fact

The `proxy-tier` Docker network already exists in production, created once on the VM outside of any Compose file:

```bash
# Create a shared network so all future apps can talk to the proxy
docker network create proxy-tier
```

This confirms the shared-reverse-proxy-network architecture: one externally managed network that this app's `web` service joins, alongside future subdomain apps. This ticket's `docker-compose.yaml` must declare `proxy-tier` as `external: true` and must not attempt to create or manage it. No further action is needed to provision the network itself; it is a solved operational prerequisite, not an open decision for this ticket.

## Problem

The user supplied a draft `docker-compose.yaml` as a starting point:

```yaml
version: '3.8'

services:
  web:
    build: .
    restart: always
    environment:
      - DEBUG=False
      - SECRET_KEY=${DJANGO_SECRET_KEY}
    volumes:
      - static_volume:/app/static
      - media_volume:/app/media
    networks:
      - proxy-tier

volumes:
  static_volume:
  media_volume:

networks:
  proxy-tier:
    external:
      name: proxy-tier
```

This draft has mismatches with the current repository and unresolved gaps that must be corrected, not copied as-is:

- **Wrong static volume path.** task-040 already defines `STATIC_ROOT = BASE_DIR / "staticfiles"`, so collected static files land at `/app/staticfiles` inside the container, not `/app/static`. `/app/static` is the source static directory baked into the image from the repository's `static/` folder (referenced by `STATICFILES_DIRS`). Mounting an empty named volume at `/app/static` would shadow the image's own source static assets and silently break `collectstatic`, since it would have nothing to collect from that path. The static volume must mount `/app/staticfiles`, matching what the entrypoint's `collectstatic --noinput` step actually populates.
- **No database is defined or referenced.** task-038 selected MySQL as the production database, but this draft has no `db` service, no database environment variables, and the application's `DATABASES` setting still points at SQLite (the MySQL settings change is task-038 Phase 1 scope, not yet implemented). Without an explicit decision, `db.sqlite3` would live inside the ephemeral container filesystem with no volume, so all data would be lost on every container recreation. This ticket must not silently ship a Compose file that appears production-ready while actually losing data on every deploy.
- **Incomplete environment configuration.** The draft only sets `DEBUG` and `SECRET_KEY`. `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` are also read from the environment by `config/settings.py` and should be set explicitly per environment rather than relying on silently falling back to their code defaults.
- **Two different `.env` mechanisms are conflated.** `${DJANGO_SECRET_KEY}` is Compose-file variable substitution, which requires a `.env` file next to the Compose file for Compose itself to read. This is separate from the application's own `python-dotenv` loading inside the container (which will find no `.env`, since it is excluded by `.dockerignore`). The ticket must pick one clear mechanism, most simply an `env_file:` entry pointing at a VM-local environment file that supplies all required variables directly to the container.
- **No mechanism for the shared reverse proxy to discover this service.** The draft attaches `web` to an `external: true` `proxy-tier` network, implying a shared reverse proxy (for example Traefik or nginx-proxy) already manages that network for multiple subdomain applications, which is consistent with task-038/task-039's future-subdomain isolation goal. However, the draft defines no routing mechanism (no Traefik labels, no `VIRTUAL_HOST`-style environment variable, and no fixed `container_name`) for that shared proxy to find and route to this service. Without one of these, the external network attachment alone does not make the site reachable.
- **Obsolete Compose file version key.** The top-level `version: '3.8'` attribute is obsolete for the Compose Specification used by modern Docker Compose v2 and produces a deprecation warning; it should be omitted.
- **No fixed container name.** Compose auto-generates a container name from the project directory, which is not guaranteed stable across environments or reproducible for a shared reverse-proxy configuration that references this service by name.

## Scope

Create a corrected, production-oriented `docker-compose.yaml` for the Django `web` service, explicitly scoped to only what task-039 Phase 1/2 requires right now.

### In scope

- Add a `docker-compose.yaml` (Compose Specification, no obsolete `version` key) defining the `web` service built from the existing `Dockerfile`.
- Declare `proxy-tier` as an `external: true` network in `docker-compose.yaml`, matching the network already created in production via `docker network create proxy-tier`; document this existing prerequisite rather than adding new creation logic.
- Fix the static volume mount to `/app/staticfiles`, matching `STATIC_ROOT`; keep the media volume mount at `/app/media`, matching `MEDIA_ROOT`.
- Set a fixed, documented `container_name` for the `web` service so a shared reverse proxy can reference it predictably.
- Replace inline `environment:` substitution with an `env_file:` reference to `.env.production`, a VM-local, non-committed environment file distinct from the existing local-dev `.env`/`.env.example` convention; document every variable it must supply: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and the `db` service's connection variables.
- Add a `db` service (MySQL) to this same Compose file on a dedicated internal application network (not `proxy-tier`), with a named `mysql_data` volume, a dedicated database and least-privilege application user sourced from `.env.production` (never MySQL root), and a health check gating `web`'s startup. Running MySQL as a sibling container avoids the Linux `host.docker.internal` connectivity gap entirely and keeps the stack self-contained for this Compose-based deployment strategy.
- Attach `web` to both the internal application network (to reach `db`) and the external `proxy-tier` network (to be reachable by the shared reverse proxy). Do not add Traefik labels, `VIRTUAL_HOST`-style variables, or any other proxy routing configuration in this ticket; that is explicitly deferred to task-039 Phase 3, which owns the actual reverse-proxy service and its routing rules.
- Keep `static_volume`, `media_volume`, and `mysql_data` as named volumes so collected static files, uploaded media, and database data persist across container recreation.
- Add a restart policy appropriate for a long-running production service and document why it was chosen.
- Add `.env.production` to `.gitignore` explicitly (the existing blanket `.env` pattern does not match `.env.production`), and provide a non-secret `.env.production.example` documenting the required variable names only.
- Document, in this ticket's own notes/README addition, that `docker compose down -v` must never be used in production teardown, since it would destroy `static_volume`, `media_volume`, and `mysql_data`.
- Document how to bring the stack up locally for verification (`docker compose config`, `docker compose up`, health check, and teardown without `-v`).

### Out of scope

- MySQL backup/restore procedures and retention policy (task-038/task-039 own the backup strategy; this ticket only provisions the `db` service and its data volume).
- Implementing the actual reverse-proxy container, TLS, and certificate renewal (task-039 Phase 3).
- Automatic deployment from `main` (task-038/task-039 Phase 4).
- Changing Django application behavior, page content, or unrelated features.
- Committing secrets, credentials, or a real `.env.production` file into the repository.

## Acceptance criteria

- [ ] `docker-compose.yaml` has no obsolete top-level `version` key and passes `docker compose config` without warnings related to it.
- [ ] The `web` service builds from the existing `Dockerfile` and uses a fixed, documented `container_name`.
- [ ] The static named volume mounts at `/app/staticfiles` (matching `STATIC_ROOT`) and is verified to contain collected static files after `docker compose up`; the media named volume mounts at `/app/media` (matching `MEDIA_ROOT`).
- [ ] The `web` service reads `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and database connection variables from an `env_file: .env.production` reference; `.env.production` is git-ignored and only a `.env.production.example` with variable names (no secret values) is committed.
- [ ] A `db` service (MySQL) runs in this Compose file with a named `mysql_data` volume, a dedicated non-root application database user, and a health check; `web` only starts serving traffic after `db` is healthy.
- [ ] `web` is attached to both the internal application network (to reach `db`) and the external `proxy-tier` network; no Traefik labels, `VIRTUAL_HOST` variables, or other proxy routing configuration are added in this ticket.
- [ ] `docker compose up -d` starts `db` and `web` successfully, applies migrations and `collectstatic` via the existing entrypoint against the containerized MySQL database, and `web` reports healthy via the existing `HEALTHCHECK`.
- [ ] No secrets, credentials, or `.env.production` values are committed to the repository.
- [ ] Documentation explicitly states that `docker compose down -v` must never be used in production teardown.
- [ ] Compose configuration and any new documentation pass a local `docker compose config` validation and a local `docker compose up`/teardown (without `-v`) smoke test.
- [ ] `python manage.py check`, the full test suite, Black, and flake8 pass against the repository state used to validate the Compose file.

## Implementation notes

- Reuse the `Dockerfile` and `entrypoint.sh` from task-040 without duplicating build or startup logic in the Compose file.
- `db` (MySQL) and its credentials, character set/collation, and least-privilege user must follow the MySQL decisions already recorded in task-038.
- `.env.production` must never be committed; only `.env.production.example` (variable names, no values) is tracked.
- Do not hardcode `SECRET_KEY`, database passwords, or other secrets into `docker-compose.yaml` itself.
- Never run `docker compose down -v` against the production stack.

## Tech-lead review

### Findings and decisions

- **Resolved: the external `proxy-tier` network is already provisioned in production.** The user confirmed it is created once per VM via `docker network create proxy-tier`, outside of any Compose file. This ticket only needs to declare it as `external: true` in `docker-compose.yaml` and document the existing prerequisite command for a fresh VM; it does not need to invent a creation step.
- **Blocking (conditional): if the "external MySQL" database story is chosen and MySQL runs on the bare Ubuntu host rather than in a container, `host.docker.internal` does not resolve automatically on Linux the way it does on Docker Desktop.** The service must either add `extra_hosts: ["host.docker.internal:host-gateway"]` (Compose spec, Docker Engine 20.10+) and use that hostname, or connect via the host's LAN/bridge IP, or simply run MySQL as a sibling container on a shared Docker network instead. Document whichever is chosen; do not assume `host.docker.internal` "just works" on the Ubuntu VM.
- **High: architecture consistency with task-039 Phase 3 wording.** task-039 currently describes configuring "Nginx server blocks... for future subdomain routing" in a way that reads as one reverse-proxy configuration per app. The external `proxy-tier` network model in this ticket implies the opposite and, in this reviewer's judgment, better architecture: a single shared reverse-proxy stack (for example Traefik or nginx-proxy) that every app's Compose project joins by attaching to the same external network, with per-app routing added via labels or generated server blocks. Recommend updating task-039 Phase 3 wording to describe "a shared reverse-proxy stack that future subdomain apps join via an external network" rather than duplicating a full proxy per app, so the two tickets do not describe contradictory architectures.
- **High: proxy discovery mechanism should be deferred here, not decided here.** Because task-039 Phase 3 already owns the actual reverse-proxy container and its routing configuration, the lowest-risk, least-duplicated-effort choice for this ticket is: do **not** add Traefik labels or `VIRTUAL_HOST`-style variables in `docker-compose.yaml` yet. Only attach `web` to the external `proxy-tier` network with a fixed `container_name`, and explicitly document that routing/labels are added when task-039 Phase 3 stands up the shared proxy. Avoid guessing a proxy technology now and having to rework labels later.
- **Medium: env file naming collision risk.** The repository already uses `.env`/`.env.example` for local `python manage.py runserver` development per `README.md`. Reusing the literal name `.env` as the Compose `env_file:` on the same VM checkout is workable (Compose reads it directly from disk; `.dockerignore` only affects the image build context, not `env_file:`) but is easy to confuse with the local dev file if anyone ever runs both on the same machine. Recommend a distinctly named file such as `.env.production` (already `.gitignore`d by the existing blanket pattern only if the pattern is updated, or added explicitly) to reduce operator confusion, and document the distinction clearly.
- **Medium: teardown safety.** Explicitly state in this ticket's documentation, not just implied from task-039, that verification/teardown during development must never use `docker compose down -v`, since that would destroy the named `static_volume`/`media_volume` (and any `db` volume, if added).

### Required design choices — resolved

- [x] `proxy-tier` external network confirmed as an existing production prerequisite (`docker network create proxy-tier`, run once per VM); this ticket documents it but does not create it.
- [x] Database story: MySQL runs as an in-Compose `db` service on an internal application network with a named volume; this avoids host MySQL entirely, so the Linux `host.docker.internal` connectivity gap does not apply.
- [x] Proxy discovery is deferred to task-039 Phase 3; this ticket only attaches `web` to the external `proxy-tier` network with a fixed `container_name` and adds no labels or `VIRTUAL_HOST`-style variables.
- [x] Env file: `.env.production`, explicitly added to `.gitignore`, with a committed `.env.production.example` listing variable names only.
- [x] `docker compose down -v` is documented as forbidden in production teardown for this stack.

If a future need reintroduces host-level MySQL or adds proxy labels directly to this file, treat that as a new decision requiring its own review rather than a silent edit.

### Review status (second pass)

**Status: unblocked.** All previously open decisions have been resolved above by explicit product-owner refinement. Implementation may proceed.

## Definition of done

- `docker-compose.yaml` builds and runs the `web` service correctly, with static/media persistence, environment-driven configuration, an explicit database story, and an explicit reverse-proxy discovery decision.
- No secrets are committed.
- The ticket is moved from `.tasks/todo/` to `.tasks/in-progress/` only when implementation begins, then to `.tasks/done/` after a successful local `docker compose up` validation.

## Implementation results

- Added `docker-compose.yaml` with Django, MySQL 8.0, persistent named volumes, an internal application network, and the externally managed `proxy-tier` network.
- Added the `volumes-init` one-shot service so the non-root image user (`1000:1000`) can collect static files into newly created named volumes.
- Added `.env.production.example`, explicitly ignored `.env.production`, and documented setup, health verification, restart behavior, and the prohibition on production `docker compose down -v`.
- Made Django select environment-driven MySQL settings when `DB_HOST` is present while preserving SQLite for local development and tests. Added the forwarded HTTPS proxy contract and MySQL 8 PyMySQL authentication dependency.
- Updated the container healthcheck to inspect local HTTP status without following the intentional production HTTPS redirect.

## Validation results

- `docker compose config --quiet` passed without a Compose version warning.
- A clean local `docker compose up -d --build` completed; MySQL became healthy, migrations ran, `collectstatic` populated 133 files, Django connected with the `mysql` backend, the production-host homepage returned `200`, and the web healthcheck became healthy.
- `python manage.py check`, all 34 tests, Black, and flake8 passed. `check --deploy` reported only the expected short smoke-test `SECRET_KEY` warning; the real production file must use a long random secret.
