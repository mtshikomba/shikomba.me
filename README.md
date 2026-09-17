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
