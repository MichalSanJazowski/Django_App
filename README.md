# Django Companies API — QA Testing Oriented Project

This project is a **Django + Django REST Framework** application created and extended **specifically for QA manual and junior automation practice**.

The application exposes REST API endpoints that allow **manual testing with Postman**, validation of HTTP behavior, and basic database verification.

---

## 🎯 Project Purpose

The main goal of this project is to practice and demonstrate:

- Manual API testing (Postman)
- Positive and negative test scenarios
- HTTP methods and status codes
- API validation issues (intentional gaps for QA testing)
- Basic database verification (SQL / ORM)
- Understanding REST principles from a QA perspective

A **dedicated test endpoint** was intentionally added to make API testing easier and more realistic for QA work.

---

## 🛠 Tech Stack

- Python 3
- Django
- Django REST Framework
- SQLite (default)
- Pytest (for backend tests)
- Postman (manual API testing)

---

## 🚀 Local Setup

```bash
git clone https://github.com/MichalSanJazowski/Django_App.git
cd Django_App
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Application will be available at:
```
http://127.0.0.1:8000/
```

---

## 🔗 API Endpoints

### Companies (REST example)
```
GET    /companies/          → list companies
POST   /companies/          → create company
GET    /companies/{id}/     → retrieve company
PATCH  /companies/{id}/     → update company
DELETE /companies/{id}/     → delete company
```

### Test Email Endpoint (QA / Postman testing)
```
POST /send-email/
```

This endpoint was **added intentionally for manual API testing in Postman**.

It allows:
- testing POST requests
- checking request body validation
- verifying status codes
- identifying missing backend validation (QA bug scenarios)

Example request body:
```json
{
  "subject": "Test subject",
  "message": "Hello world"
}
```

---

## 🧪 Manual Testing with Postman (QA Focus)

This project is suitable for practicing:

- Correct vs incorrect request payloads
- Missing required fields
- Invalid HTTP methods (405 Method Not Allowed)
- Status codes: 200, 201, 400, 404, 405
- REST rules (collection vs resource endpoints)
- Bug reporting (validation issues, incorrect responses)

---

## 🧠 Example QA Findings

- Missing required fields may still return `200 OK` → **validation bug**
- DELETE on collection endpoint returns `405` → **correct REST behavior**
- DELETE on resource endpoint works as expected

---

## 🧪 Automated Tests (Optional)

Basic pytest configuration is included for backend-side testing.
Manual API testing with Postman is the primary focus of this project.

---

## 📌 Notes

- Authentication was intentionally omitted to simplify manual testing.
- The project is designed as a **QA sandbox**, not a production-ready system.

---

## 👤 Author

Developed by **Michal Sanak-Jazowski**  
QA Manual / Junior Automation practice project
