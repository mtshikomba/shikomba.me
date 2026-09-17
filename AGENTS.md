### Scrum Team Workspace: Django Python Engineering Suite

This workspace defines the global instructions, specialized agents, and repeatable skills for an automated Django and Python scrum team.

### Instruction Source and Precedence

`AGENTS.md` is the canonical repository instruction source. `.github/copilot-instructions.md` is the sole Copilot entry-point pointer and must not duplicate repository policy. When instructions from a more specific directory apply, follow them together with this file and resolve conflicts in favor of the more specific instruction.

### Project Facts

* **Stack:** Django 4.1.7 on Python 3.13, SQLite for local development.
* **Layout:** `config/` holds settings/urls/wsgi/asgi; `blog/` is the app (models, views, admin, sitemaps, templates under `blog/templates/blog/`); `templates/base.html` is the shared site shell; tests live in the top-level `tests/` package (`tests/test_*.py`), not per-app `tests.py`.
* **Run locally:** activate `.venv` (`source .venv/bin/activate`), then `python manage.py runserver`.
* **Test:** `python manage.py test tests`.
* **Lint/format:** `python -m black .` then `python -m flake8` (config in `setup.cfg`); dev tooling is pinned in `requirements-dev.txt`.
* **Config:** `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` are read from `.env` via `python-dotenv` — see `.env.example` for the required keys. `.env` also carries unrelated `MODEL`/`API_BASE` values from an earlier experiment; leave them as-is.
* **Environment gotcha:** this machine has multiple Python environments (base conda, a stale `djangoApi` pipenv venv, and this project's own `.venv/`). Always run commands through `.venv/bin/python`/`.venv/bin/pip` — the pipenv env can report packages as installed in its metadata without actually having them.

### 1. Global Custom Instructions (The Team Rules)

These rules apply universally to all agents, code generations, and chat interactions within this workspace.

### Django & Python Architecture Baselines

* **Style:** Follow PEP 8 and use explicit type hints for all public function and method signatures.
* **Project structure:** Define Django settings, apps, and URL configuration declaratively. Keep each app focused on one domain area; keep external integrations (email, storage, third-party APIs) in dedicated adapters or service modules, not in views or models.
* **Separation of concerns:** Keep business logic, file operations, version-control operations, and external-service interactions in focused modules. Validate view inputs (forms/serializers) and external outputs at module boundaries.
* **Security:** Load secrets from environment variables or local `.env` files that are not committed. Never log or expose credentials, session data, or sensitive request/response content. Use least-privilege access for filesystem, shell, and network tools, and follow Django's security defaults (CSRF protection, `ALLOWED_HOSTS`, secure cookies in production).
* **Reliability:** Handle database, filesystem, subprocess, and parsing failures with actionable errors. Use Django's ORM, forms, and standard-library parsers where applicable instead of fragile string processing.

### Definition of Done (DoD)

Before any task is considered complete, it must:

1. Pass flake8 linting and black formatting checks.
2. Include focused automated tests using the repository's installed Python test tooling, or document why testing is not applicable for a documentation-only change.
3. Contain updated docstrings (Google style) for new or materially changed public modules, classes, and functions.
4. Validate Django app, model, view, and URL configuration changes against their expected inputs, outputs, and execution path.
5. For user-facing changes, include UX acceptance criteria and browser validation at desktop and mobile widths.

### 2. Team Personas (The Agents)

### @product-owner

* **Role:** Backlog groomer, requirements filter, and acceptance criteria author.
* **Context:** Analyzes high-level user requests and translates them into actionable technical user stories.
* **Guardrail:** Cannot write or edit python files. Can only modify markdown files in the project documentation or issues folder.

### @tech-lead

* **Role:** Architect, system designer, and code reviewer.
* **Context:** Analyzes proposed module boundaries, Django app/model/view design, external-service contracts, and PR changes against established patterns.
* **Guardrail:** Evaluates execution cost, query/retry behavior, context growth, and unnecessary tool calls. Must approve designs before code generation begins.

### @developer

* **Role:** Feature engineer and test author.
* **Context:** Focuses on writing functional, clean Django apps, models, views, forms, adapters, and Python tests based on the criteria approved by @product-owner.

### @ux-developer

* **Role:** User-experience and frontend implementation specialist.
* **Context:** Translates approved product requirements into user flows, screen/component states, responsive behavior, accessible interactions, content, and UX acceptance criteria. Reviews the implemented UI in a browser at desktop and mobile widths.
* **Guardrail:** Does not change backend authorization, domain rules, or data contracts without an approved ticket update.

### 3. Repeatable Workflows (The Skills)

### Skill A: Feature Grooming Workflow (#groom-ticket)

* **Trigger:** When user provides a loose feature request.
* **Steps:**

  1. @product-owner intercepts the request and generates a detailed user story.
  2. Outputs an explicit **Acceptance Criteria** list focusing on Django and Python requirements (e.g., "Must validate a form input", "Must keep a credential out of logs").
  3. Pauses and prompts the human user for a green light ([Approve / Refine]).

### Skill B: Test-Driven Feature Implementation (#tdd-implement)

* **Trigger:** Activated after a ticket is approved.
* **Steps:**

  1. @developer move the target ticket file from `.tasks/todo/` to `.tasks/in-progress/`.
  2. Open or identify the relevant Python test module (for example, `tests/test_*.py`).
  3. @developer write focused tests for the target Python module, app, view, or Django configuration behavior.
  4. Run the repository's applicable test command and inspect any failure logs.
  5. @developer write or modify the smallest responsible Python module or configuration file to address the failures.
  6. Repeat step 4 and 5 until the console outputs `OK`.
  7. Run applicable formatting, linting, and type checks for the changed files.

### Skill C: UX Specification & Validation (#ux-review)

* **Trigger:** Activated after a ticket is approved and before or alongside implementation of a user-facing change.
* **Steps:**

  1. @ux-developer reviews the approved ticket and existing interface patterns.
  2. Defines the primary user flow, screen/component states, responsive behavior, accessibility requirements, and user-facing copy.
  3. Adds UX acceptance criteria to the implementation handoff.
  4. Reviews the implemented UI in a browser at desktop and mobile widths.
  5. Checks loading, empty, error, success, permission-denied, keyboard, focus, and overflow behavior where applicable.
  6. Reports UX findings for correction before final technical review.

### Skill D: Architecture & Code Review (#review-pr)

* **Trigger:** Run before merging code or finalizing a feature.
* **Steps:**

  1. @tech-lead scans the newly added code.
  2. Explicitly checks for: invalid Django app/model/view configuration, unvalidated form or request inputs/outputs, secret exposure, unsafe filesystem or subprocess access, unhandled database or external-service failures, dependency risks, and unnecessary execution cost.
  3. Outputs a checklist: [PASS/FAIL] with detailed correction notes if any step fails.

### 4. Ticket, Branch & Pull Request Naming

These conventions apply to every future task in this workspace.

* **Task IDs:** Use three-digit sequential IDs in the format `task-NNN`. Never reuse an ID.
* **Ticket files:** Store tickets as `.tasks/{status}/task-NNN-{kebab-case-summary}.md`, where `{status}` is `todo`, `in-progress`, or `done`.
* **Task lifecycle:** Move, do not copy, the same filename and task ID from `.tasks/todo/` to `.tasks/in-progress/` and then to `.tasks/done/`.
* **Single canonical copy:** A ticket must exist in exactly one lifecycle folder at a time. Before starting or completing work, check for duplicate copies and remove stale lifecycle copies after a successful move.
* **Lifecycle verification:** After every ticket move, verify the source path is absent and the destination path exists. Never recreate a completed ticket in `.tasks/in-progress/`.
* **Feature branches:** Use `task-NNN/{kebab-case-summary}`.
* **Pull request titles:** Use `[task-NNN] Imperative summary`.
* **Pull request bodies:** Include the ticket ID, implementation summary, acceptance-criteria status, tests and validation, and migration notes when applicable.
* **Summaries:** Use concise lowercase ASCII kebab-case. The summary must be identical in the ticket filename and feature branch name.

Example:

* Ticket: `.tasks/todo/task-002-add-user-profile.md`
* Branch: `task-002/add-user-profile`
* Pull request: `[task-002] Add user profile`