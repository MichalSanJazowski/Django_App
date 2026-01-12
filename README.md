# Django Companies API — Testing-Oriented README

A small Django + Django REST Framework application for managing companies, with a simple email-sending endpoint.  
This README is **focused on testing** (manual + automated): setup, API behavior, pytest usage, and CI.

---

## Table of Contents
- Features
- Tech Stack
- Requirements
- Local Setup
- Environment Variables
- API Endpoints
- Testing with pytest
- CI (GitHub Actions)
- Common Issues

---

## Features
- CRUD for `Company` via DRF `ModelViewSet`
- Default ordering by `last_update` (descending)
- `POST /send-email` endpoint (email sending)
- Test-friendly email handling (locmem backend + mocks)

---

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (default)
- pytest + pytest-django
- python-dotenv

---

## Requirements
- Python **3.12** (matches CI)
- pip

---

## Local Setup

1) Clone the repo or unzip the archive.

2) Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3) Install dependencies:
```bash
pip install -r requirements.txt
```

4) Configure environment variables (see below).

5) Run migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

---

## Environment Variables

Loaded from `.env` (via `python-dotenv`) or the system environment.

Required:
- `DJANGO_SECRET_KEY` — required by Django

Optional (only if you want real SMTP sending):
- `EMAIL_HOST_PASSWORD`

Example `.env`:
```env
DJANGO_SECRET_KEY=dev-secret-key-change-me
EMAIL_HOST_PASSWORD=dummy
```

> **Testing note:**  
> Emails are handled safely in tests using:
> - Django `locmem` email backend (`mailoutbox`)
> - Mocking `send_mail` (no external calls)

---

## API Endpoints

### Companies (DRF router)
- `GET /companies/` — list companies
- `POST /companies/` — create a company
- `GET /companies/{id}/` — retrieve details
- `PUT/PATCH /companies/{id}/` — update
- `DELETE /companies/{id}/` — delete

**Company fields:**
- `name` (unique)
- `status` (Layoffs / Hiring Freeze / Hiring)
- `last_update`
- `application_link` (URL)
- `notes`

### Send Email
- `POST /send-email`
  - JSON body:
    ```json
    { "subject": "Subject", "message": "Message" }
    ```
  - In tests: mocked / locmem backend

---

## Testing with pytest

### Run tests
```bash
pytest -q
```

### Pytest configuration
- `pytest.ini` sets `DJANGO_SETTINGS_MODULE=mysite.settings`
- Test file patterns:
  - `tests.py`
  - `test_*.py`
  - `*_tests.py`

### Test structure
- `companies/tests/test_api.py`
  - API tests for `/companies/`
  - Validation errors (400), choices, defaults
  - Examples of `xfail`, `skip`, `pytest.raises`, and logging (`caplog`)
- `companies/tests/test_emails.py`
  - Email sending with `mailoutbox`
  - `/send-email` endpoint with mocked `send_mail`
  - Method restriction test (405 for GET)

### Writing new tests (tips)
- API tests: use `client` fixture (`pytest-django`)
- Database access: mark with `@pytest.mark.django_db`
- Email tests: prefer `mailoutbox` or mock `send_mail`

---

## CI (GitHub Actions)

CI runs on:
- `push`
- `pull_request`

Steps:
1. Install dependencies
2. `python manage.py migrate --noinput`
3. `pytest -q`

CI uses **Python 3.12**.  
Secrets like `DJANGO_SECRET_KEY` and `EMAIL_HOST_PASSWORD` are stored in **GitHub Secrets**.

---

## Common Issues

### SECRET_KEY missing
Add `DJANGO_SECRET_KEY` to `.env` or set it in your environment.

### Emails sent outside tests
Ensure tests use the `locmem` email backend or mocks.  
If modified, restore:
```python
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
```

### Python version mismatch
Use Python 3.12 locally to match CI behavior.A

---

## Author
Educational/testing project: Django + DRF + pytest.
