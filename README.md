# shikomba.me

Personal blog built with Django, intended to be deployed at `shikomba.me`.

## Requirements

- Python 3.13

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env  # then fill in SECRET_KEY, etc.
python manage.py migrate
```

## Run

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/. Create an admin user with `python manage.py createsuperuser` to author posts at `/admin/`.

## Test

```bash
python manage.py test tests
```

## Lint & format

```bash
black .
flake8
```

## Project layout

- `config/` — Django settings, URLs, WSGI/ASGI entry points
- `blog/` — the blog app (models, views, admin, sitemaps, templates)
- `templates/base.html` — shared site shell
- `tests/` — automated tests

## Configuration

Environment variables (via `.env`, see `.env.example`):

- `SECRET_KEY`, `DEBUG`
- `ALLOWED_HOSTS` — comma-separated hosts (defaults include `shikomba.me`, `www.shikomba.me`)
- `CSRF_TRUSTED_ORIGINS` — comma-separated origins

## Production Docker Compose

The production Compose stack runs Django and MySQL as sibling services. The
application joins the externally managed `proxy-tier` network, which must be
created once on the VM with `docker network create proxy-tier`; Compose does
not create or remove that network. Proxy routing is configured separately by
the shared reverse-proxy deployment.

Create the VM-local environment file from the non-secret template and replace
all placeholder values, especially the passwords:

```bash
cp .env.production.example .env.production
docker compose config
docker compose up -d
docker compose ps
docker compose logs web
```

The `web` service uses the fixed container name `shikomba-web` and runs with
`restart: unless-stopped`, so it returns after ordinary host or Docker daemon
restarts while still allowing an operator to stop it deliberately. The
`static_volume`, `media_volume`, and `mysql_data` named volumes persist data;
the application user in the image uses UID/GID `1000:1000`.

For local verification, stop the stack with `docker compose down` and leave
the named volumes in place. Never run `docker compose down -v` in production:
it destroys the collected static files, uploaded media, and MySQL data.
