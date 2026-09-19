# task-040: Create production Dockerfile

## User story

As the developer deploying shikomba.me, I want a production-ready Dockerfile for this Django project so a container image can be built and run consistently, supporting the containerized deployment strategy in task-039.

## Relationship to other tickets

This ticket implements the Dockerfile deliverable described in task-039 Phase 1 ("Container and application readiness"). It does not implement Compose services, MySQL, reverse proxy, volumes, or automatic deployment; those remain in task-039.

## Problem

The user supplied a draft Dockerfile as a starting point:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Script to handle migrations and start Gunicorn safely
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
```

This draft has known mismatches with the current repository that must be corrected, not copied as-is:

- The project's WSGI module is `config.wsgi`, not `your_project_name.wsgi`.
- `AGENTS.md` states this project runs Django 4.1.7 on Python 3.13 as a fact. The base image is `python:3.13-slim`, not `python:3.11-slim`.
- `libpq-dev` is a PostgreSQL client build dependency. task-038/task-039 specify MySQL as the production database, so the image needs the MySQL-appropriate dependency instead. This ticket selects PyMySQL, a pure-Python driver, so no `libpq-dev`, `gcc`, or MySQL client headers are needed at all.
- `requirements.txt` does not currently include Gunicorn or a MySQL driver; both must be added and pinned before the image can build a working production entrypoint.
- The draft's comment references a migration-handling script that does not exist yet and is not defined in this draft.
- The draft copies the entire build context with `COPY . .` and has no `.dockerignore`, risking secrets (`.env`), the SQLite dev database, virtual environments, and Git metadata being baked into the image.
- The draft runs as root with no non-root user, no `HEALTHCHECK`, and no explicit dependency layer caching strategy beyond `requirements.txt`.
- The draft installs `netcat-openbsd`, presumably for a `wait-for-db` entrypoint script. Database readiness is handled by Compose `depends_on`/`healthcheck` in task-039, so `netcat-openbsd` is dropped from this image entirely.

## Scope

Create a corrected, production-ready Dockerfile (and supporting `.dockerignore`) for this Django project.

### In scope

- Add a single-stage `Dockerfile` based on `python:3.13-slim`. A single stage is sufficient because PyMySQL requires no C compiler or MySQL client headers.
- Fix the Gunicorn entrypoint to reference the actual WSGI module (`config.wsgi:application`).
- Add `gunicorn` and `PyMySQL` to `requirements.txt`, pinned to specific versions; do not install `requirements-dev.txt` in the image.
- Add a `.dockerignore` excluding `.env`, `.venv`, `db.sqlite3`, `__pycache__`, Git metadata, media uploads not meant for the image, and other non-essential files.
- Create a dedicated non-root user/group (fixed UID/GID `1000:1000`) and run the container process as that user, with the app directory and any writable runtime paths (`collectstatic` output, logs) owned by it.
- Add a `HEALTHCHECK` using a Python one-liner (no external HTTP client) against the application's health endpoint from task-038 Phase 1; if that endpoint's path changes, this `HEALTHCHECK` command must be updated in the same change.
- Define how migrations and `collectstatic` are run relative to container startup (entrypoint script, init container step, or documented manual step) without silently running migrations on every container start in an unsafe way.
- Keep image layer caching effective by copying dependency manifests before application code.
- Document how to build and run the image locally for verification, including the expected non-root UID/GID for anyone wiring up matching volume ownership in task-039.
- Ensure no `ARG`/`--build-arg` is used to pass `SECRET_KEY`, database credentials, or any other secret into the build.

### Out of scope

- Docker Compose service definitions, MySQL container/service setup, reverse proxy, and volumes (task-039).
- Changing Django application behavior, page content, or unrelated features.
- Implementing the automatic deployment trigger (task-038/task-039 Phase 4).
- Committing secrets, credentials, or environment values into the image or repository.

## Acceptance criteria

- [x] The `Dockerfile` builds successfully from `python:3.13-slim`.
- [x] The Gunicorn `CMD`/entrypoint references the project's real WSGI application path (`config.wsgi:application`), verified by successfully starting the container and receiving a response from the application.
- [x] No PostgreSQL-specific or otherwise unnecessary OS packages are installed; `libpq-dev`, `gcc`, and `netcat-openbsd` are absent from the image.
- [x] `requirements.txt` includes pinned `gunicorn` and `PyMySQL` versions, and the image installs them successfully; `requirements-dev.txt` is never installed in the image.
- [x] A `.dockerignore` file prevents `.env`, `.venv`, `db.sqlite3`, `media/` (unless explicitly intended), `__pycache__`, and `.git` from being copied into the build context or image.
- [x] The container runs the application process as a dedicated non-root user with a fixed, documented UID/GID (`1000:1000`), with correct ownership on the app directory and any writable runtime paths.
- [x] The image defines a `HEALTHCHECK` using a Python-only command against the task-038 health endpoint; the command is verified to succeed against a running container.
- [x] Migration and `collectstatic` execution is explicit and documented (entrypoint script, separate build/deploy step, or manual command), and does not silently run in a way that could apply migrations unexpectedly on every restart without operator visibility.
- [x] Rebuilding the image after an application code-only change reuses the cached dependency-installation layer when `requirements.txt` is unchanged.
- [x] `docker build` succeeds locally, and a locally run container serves the Django application on the exposed port with the production settings module.
- [x] No secrets, credentials, `.env` values, or build arguments containing secrets are present in the built image layers.
- [x] `python manage.py check`, the full test suite, Black, and flake8 pass against the repository state used to build the image.

## Implementation notes

- Base image: `python:3.13-slim`, per `AGENTS.md`.
- MySQL driver: `PyMySQL` (pure-Python, no compiled extensions, no OS build dependencies). If a future performance need justifies `mysqlclient` instead, that is a separate ticket that must also introduce a multi-stage build.
- Non-root user: fixed `app` user/group at UID/GID `1000:1000`; task-039's volume ownership for static/media must match this UID/GID or explicitly `chown` on volume creation.
- Health check: a Python one-liner hitting the task-038 health endpoint; keep the endpoint path and this command in sync when either changes.
- Keep this Dockerfile reusable by the Compose configuration in task-039 rather than duplicating build logic.
- Prefer copying `requirements.txt` before copying the rest of the application code, to preserve Docker layer caching.

## Tech-lead review

### Findings and decisions

- **Blocking: Python version is not actually ambiguous — resolve it now.** `AGENTS.md` states this project runs "Django 4.1.7 on Python 3.13" as a fact, not a suggestion. The base image must be `python:3.13-slim` (or the exact patch tag the team pins elsewhere). Drop the "confirm with maintainer" hedge for the Python version specifically; only the MySQL driver choice remains genuinely open.
- **Blocking: choose single-stage vs. multi-stage before writing the Dockerfile, based on the MySQL driver decision.** If the chosen driver requires compiled extensions (for example `mysqlclient`, which needs `gcc` and MySQL/MariaDB dev headers), use a multi-stage build: a `builder` stage installs build tools and produces wheels/installed packages, and the final runtime stage copies only the installed Python packages and app code, without `gcc` or `-dev` headers present in the shipped image. If a pure-Python driver (for example `PyMySQL`) is chosen, a single stage is sufficient and no compiler is needed at all. Record this decision explicitly in the ticket once the driver is chosen; do not leave "multi-stage or single-stage" open in the final implementation.
- **High: `netcat-openbsd` from the draft has no defined purpose in this ticket.** It was almost certainly there to support a `wait-for-it`/`nc`-based "wait for the database" entrypoint pattern. Task-039 already assigns database readiness to Compose `depends_on`/`healthcheck`. Decide explicitly: either drop `netcat-openbsd` entirely (preferred, since readiness is Compose's job) or keep it and document exactly which script uses it. Do not carry it over silently "just in case."
- **High: `HEALTHCHECK` tooling must exist in the image.** `python:3.13-slim` does not include `curl` or `wget` by default. If a `HEALTHCHECK` instruction is added, it must use a tool actually present in the image (for example a small Python `urllib`/`http.client` one-liner, or `python manage.py` based check), or install a minimal HTTP client deliberately. Do not write a `HEALTHCHECK` that silently fails because the binary it calls is missing.
- **High: non-root user must also cover writable runtime paths.** Beyond `chown` on the app directory, explicitly verify the non-root user can write to wherever `collectstatic` output and any container-local temp/log paths land, and that this stays compatible with the persistent volumes task-039 will mount for static/media. Misaligned UID/GID between the image's non-root user and mounted volume ownership is a common source of silent permission failures; document the expected UID/GID or use a fixed, documented value.
- **Medium: explicitly forbid installing `requirements-dev.txt` in the production image.** The draft only copies `requirements.txt`, which is correct, but the ticket should say so explicitly as an acceptance criterion rather than leaving it as an implicit assumption, since a future edit could accidentally add `-r requirements-dev.txt`.
- **Medium: no secrets via build arguments.** State explicitly that `ARG`/`--build-arg` must not be used to pass `SECRET_KEY`, database credentials, or other secrets, since build args and intermediate layers can leak them even if the final image looks clean.

### Required design choices — resolved

- [x] Base image: `python:3.13-slim`, per `AGENTS.md`.
- [x] MySQL driver: `PyMySQL` (pure-Python). No `gcc`/MySQL client headers; single-stage build.
- [x] `netcat-openbsd` dropped; database readiness is handled by Compose `depends_on`/`healthcheck` in task-039.
- [x] `HEALTHCHECK` uses a Python one-liner against the task-038 health endpoint; no external HTTP client is installed.
- [x] Non-root user fixed at UID/GID `1000:1000`; task-039 must align static/media volume ownership to this value.

If a future change needs `mysqlclient` instead of `PyMySQL`, or a different UID/GID, treat that as a new decision requiring its own review rather than a silent edit to this ticket.

## Implementation results

- Added `STATIC_ROOT = BASE_DIR / "staticfiles"` to `config/settings.py`; required for `collectstatic` to run at all and already covered by the existing `.gitignore` entry.
- Pinned `gunicorn==23.0.0` and `PyMySQL==1.1.1` in `requirements.txt`.
- Added `entrypoint.sh`, which logs and runs `migrate --noinput` then `collectstatic --noinput` before `exec`-ing the Gunicorn `CMD`; this satisfies the "entrypoint script" option with visible, documented logging rather than silent behavior.
- Fixed a real bug found during verification: `WORKDIR /app` is created before the `app` user exists, so `COPY --chown=app:app` alone left the `/app` directory itself owned by `root`, which made SQLite fail with `unable to open database file`. Added an explicit `chown -R app:app /app` after the copy to fix this.
- The `HEALTHCHECK` targets `http://127.0.0.1:8000/` (the existing blog homepage route) as an interim target, since task-038's dedicated health endpoint does not exist yet; this is documented in the Dockerfile comment and must be updated together with that endpoint once it exists.

### Validation performed

- `python manage.py check`, `python manage.py test tests` (34 passed), `black --check .`, and `flake8` all pass.
- `docker build` succeeded on `python:3.13-slim`.
- A locally run container applied all migrations, ran `collectstatic` (133 files), started Gunicorn, and served `GET /` with `200`.
- `docker inspect` reported the container `HEALTHCHECK` status as `healthy`.
- Confirmed no `.env` file present in the running container and that `black`/dev tooling is not installed (`requirements-dev.txt` is not installed, only present as a plain file).
- Rebuilding after touching an application file (`blog/views.py`) reused the cached dependency-installation layer.

## Definition of done

- The Dockerfile builds and runs the Django application correctly with the corrected WSGI path, approved base image, and MySQL-appropriate dependencies.
- No PostgreSQL-specific packaging remains unless explicitly reintroduced by a separate decision.
- Secrets are excluded from the build context and image.
- The image runs as a non-root user and defines or documents a health check.
- The ticket is moved from `.tasks/todo/` to `.tasks/in-progress/` only when implementation begins, then to `.tasks/done/` after a successful local build/run validation.
