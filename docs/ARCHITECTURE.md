# DEEPAK INTERVIEW HUB — Software Architecture Document

**Brand Name:** DEEPAK  
**Product Name:** Deepak Interview Hub  
**Tagline:** Learn. Practise. Test. Get Interview Ready.

---

## 1. Architectural Style

Deepak Interview Hub employs a clean, layered RESTful architecture:
- **Frontend Presentation Layer:** Semantic HTML5, mobile-first CSS3 using CSS Custom Properties design tokens, and modular Vanilla ES6+ JavaScript. No unnecessary framework bloat.
- **Backend Application Layer:** Python 3.12 with Django 6.1 and Django REST Framework (DRF) 3.18, organized into domain-driven apps (`accounts`, `content`, `practice`, `assessments`, `progress`, `dashboard`).
- **Database Persistence Layer:** PostgreSQL for production; SQLite for local development.

```
Client Tier (HTML/CSS/JS)
         ↓  (JSON / HTTP REST over Fetch API)
Django REST Framework Tier (ViewSets / APIViews / Serializers)
         ↓  (Services & Business Logic)
Django ORM Data Access Tier
         ↓  (Parameterized SQL)
Database (PostgreSQL / SQLite)
```

---

## 2. Directory Layout

```
G:\websites\interview prep\
├── backend/                          # Django application root
│   ├── manage.py
│   ├── config/                       # Settings and root routing
│   │   ├── settings/
│   │   │   ├── base.py              # Shared configuration
│   │   │   ├── development.py       # SQLite & debug config
│   │   │   └── production.py        # PostgreSQL & HTTPS config
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── accounts/                 # User auth & student profiles
│   │   ├── content/                  # Subjects, topics, questions, options
│   │   ├── practice/                 # Coding sandbox, SQL exercises
│   │   ├── assessments/              # Timed mock tests, attempts, scoring
│   │   ├── progress/                 # Bookmarks, progress tracking, activity
│   │   └── dashboard/                # Real-time analytics aggregation
│   └── requirements/                 # Dependency definitions
├── frontend/                         # Client presentation tier
│   ├── index.html                    # Homepage / Landing
│   ├── pages/                        # Specialized view modules
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── subjects.html
│   │   ├── questions.html
│   │   ├── mock-test.html
│   │   ├── mock-test-attempt.html
│   │   ├── mock-test-result.html
│   │   ├── coding-practice.html
│   │   ├── sql-practice.html
│   │   ├── bookmarks.html
│   │   ├── hr-prep.html
│   │   ├── project-viva.html
│   │   └── aptitude.html
│   ├── css/
│   │   ├── design-system.css         # Tokens, reset, typography
│   │   ├── components.css            # 18 Reusable UI components
│   │   └── layout.css                # Responsive navigation & grids
│   └── js/
│       ├── api/client.js             # Token-authenticated fetch client
│       ├── utils/toast.js            # Notification alerts
│       ├── components/navbar.js      # Responsive drawer & sticky nav
│       └── pages/                    # Page-specific controllers
└── docs/                             # Engineering documentation
```

---

## 3. Layered Design Principles

1. **Separation of Concerns:** Business logic resides in backend services/views; presentation components only render state and trigger API dispatches.
2. **Assessment Integrity:** Mock test question generators do not send correct answers to the browser. Answer verification and score computation occur exclusively on the backend server.
3. **No Fake Statistics:** Dashboards aggregate real records from `TestAttempt` and `StudentProgress`. When a user is new, informative empty states guide them to practice.

