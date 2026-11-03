# DEEPAK INTERVIEW HUB — Security Architecture & Guidelines

---

## 1. Authentication & Password Security
- Passwords hashed using Django's default PBKDF2 algorithm with SHA-256 hash.
- Minimum length of 8 characters enforced at serializer and model levels.
- Token authentication (`TokenAuthentication`) with per-user cryptographic token keys.
- Tokens cleared on logout (`POST /api/auth/logout/`).

## 2. Assessment Integrity & Anti-Tampering
- Assessment question endpoints (`/api/mock-tests/generate/`) do NOT return correct answer fields (`correct_answer`, `explanation`, `is_correct`) in the JSON response payload.
- Grading is calculated entirely on the server side (`/api/mock-tests/submit/`).
- Scores or marks passed by client requests are ignored; the server counts matches against the relational database directly.

## 3. SQL Injection Prevention
- All database queries are executed via the Django ORM using parameterized SQL queries.
- Raw SQL execution with unsanitized string formatting is prohibited.

## 4. Cross-Site Scripting (XSS) & Input Sanitization
- Django template engine auto-escapes HTML characters.
- Frontend JavaScript applies strict `escapeHtml()` utility functions when rendering user inputs or dynamic code snippets.

## 5. Cross-Origin Resource Sharing (CORS) & Production Headers
- Development settings allow all origins for easy local testing.
- Production settings (`config.settings.production`) enforce:
  - `CORS_ALLOW_ALL_ORIGINS = False` with strict whitelist.
  - `SECURE_SSL_REDIRECT = True`
  - `SESSION_COOKIE_SECURE = True`
  - `CSRF_COOKIE_SECURE = True`
  - `X_FRAME_OPTIONS = 'DENY'`
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`

