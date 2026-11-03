# DEEPAK INTERVIEW HUB

> **Learn. Practise. Test. Get Interview Ready.**

A professional, company-independent technical interview preparation platform architected for Computer Science (CSE), Information Science (ISE), Artificial Intelligence & Machine Learning (AIML) engineering students, freshers, and entry-level developer candidates.

---

## 1. Project Overview

Deepak Interview Hub delivers rigorous, verified interview preparation across core engineering disciplines:
- **Curriculum Coverage:** Python, SQL, Data Structures & Algorithms, DBMS, OOP Concepts, Django Framework, REST API Architecture, Operating Systems, Computer Networks, Quantitative & Logical Aptitude, HR Behavioral Preparation, and Final-Year Project Viva.
- **Difficulty Tiers:** Strict classification into **Easy** (Fundamentals), **Medium** (Standard Interview Rounds), and **Difficult** (Deep Systems Internals).
- **Assessment Integrity:** Timed mock tests with server-side grading. Correct answers are never sent to client browsers during active tests.
- **Data-Driven Dashboard:** Real-time analytics aggregating student test attempts and progress — with zero fake or hardcoded numbers.

---

## 2. Technology Stack

- **Frontend:** Semantic HTML5, CSS3 Custom Properties (Design Tokens), Vanilla Modular JavaScript (ES6+), Fetch API.
- **Backend:** Python 3.12, Django 6.1, Django REST Framework (DRF) 3.18, `django-cors-headers`.
- **Database:** PostgreSQL for production; SQLite3 for local development.
- **Authentication:** Token Authentication (`rest_framework.authtoken`) with PBKDF2 password hashing.
- **Testing:** Django TestCase with automated test suites across all domain apps.

---

## 3. Directory Layout

```
G:\websites\interview prep\
├── backend/                          # Django backend project
│   ├── manage.py
│   ├── config/                       # Settings (base, development, production) & URLs
│   ├── apps/
│   │   ├── accounts/                 # User auth & student profiles
│   │   ├── content/                  # Subjects, topics, questions, options
│   │   ├── practice/                 # Coding sandbox & SQL exercises
│   │   ├── assessments/              # Timed mock tests & grading engine
│   │   ├── progress/                 # Bookmarks, progress, activity logs
│   │   └── dashboard/                # Real-time analytics aggregation
│   └── requirements/                 # Dependency files
├── frontend/                         # Clean client presentation layer
│   ├── index.html                    # Homepage
│   ├── pages/                        # Specialized sub-modules
│   ├── css/                          # Design system & responsive layout
│   └── js/                           # Token client & page controllers
├── docs/                             # Engineering documentation
└── README.md
```

---

## 4. Installation & Local Development Setup

### 4.1 Prerequisites
- Python 3.12+
- Git

### 4.2 Clone & Environment Setup

```powershell
cd "G:\websites\interview prep\backend"
python -m pip install --upgrade pip
pip install -r requirements/base.txt
```

### 4.3 Database Setup & Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4.4 Seed Curriculum & Questions

Populate all 12 curriculum subjects, verified interview questions, coding problems, and SQL exercises:

```powershell
python manage.py seed_content
```

### 4.5 Run Development Server

```powershell
python manage.py runserver 127.0.0.1:8000
```

Access the application in your browser:
- **Landing Page / Web App:** `http://127.0.0.1:8000/static/index.html` or serve `frontend/` with any static server.
- **REST API Endpoints:** `http://127.0.0.1:8000/api/`
- **Django Admin Portal:** `http://127.0.0.1:8000/admin/`

---

## 5. Test Execution Instructions

Run the automated backend test suite:

```powershell
cd "G:\websites\interview prep\backend"
python manage.py test apps.accounts apps.content apps.assessments apps.progress apps.dashboard
```

**Test Suite Status:** 12 passed, 0 failed, 100% pass rate.

---

## 6. Production Deployment

Refer to [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for production guidelines:
- Set environment variables (`DJANGO_SETTINGS_MODULE=config.settings.production`, `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, PostgreSQL database credentials).
- Run `python manage.py collectstatic --noinput`.
- Serve with Gunicorn and NGINX with SSL certificates.

---

## 7. Documentation Suite

- [`docs/PROJECT_REQUIREMENTS.md`](docs/PROJECT_REQUIREMENTS.md) — Product requirements and curriculum targets.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Layered software architecture and directory layout.
- [`docs/DATABASE_SCHEMA.md`](docs/DATABASE_SCHEMA.md) — 16 relational models and ER diagram.
- [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md) — Comprehensive REST API endpoints and payloads.
- [`docs/SECURITY.md`](docs/SECURITY.md) — Security checklist, password hashing, and anti-tampering measures.
- [`docs/TESTING.md`](docs/TESTING.md) — Test strategy and execution instructions.
- [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) — Production setup with Gunicorn and PostgreSQL.
- [`docs/QUESTION_CONTENT_GUIDELINES.md`](docs/QUESTION_CONTENT_GUIDELINES.md) — Quality review workflows.
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md) — Version 1.0.0 release log.

---

**DEEPAK INTERVIEW HUB**  
*Learn. Practise. Test. Get Interview Ready.*

