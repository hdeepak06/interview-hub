# DEEPAK INTERVIEW HUB — Testing Strategy & Test Execution

---

## 1. Test Suite Architecture

The test suite covers:
- **Authentication & Profiles:** User registration with branch selection, duplicate username/email prevention, credential validation, token assignment.
- **Content Gating & Filtering:** Only published questions exposed via API; draft questions properly isolated; subject and difficulty filtering verified.
- **Assessment Scoring Integrity:** Safe delivery of test questions (no answer leakage) and server-side grading accuracy.
- **Progress & Bookmarks:** Adding, listing, deduplication, and removal of saved questions.
- **Dashboard Aggregations:** Verification that new student accounts show real zero-state metrics without fake statistics.

---

## 2. Running Automated Tests

To run the complete automated test suite:

```powershell
cd "G:\websites\interview prep\backend"
python manage.py test apps.accounts apps.content apps.assessments apps.progress apps.dashboard
```

### Verified Test Results

```
Creating test database for alias 'default'...
............
----------------------------------------------------------------------
Ran 12 tests in 10.823s

OK
Destroying test database for alias 'default'...
Found 12 test(s).
System check identified no issues (0 silenced).
```

