# DEEPAK INTERVIEW HUB — REST API Specification

**Base URL:** `http://127.0.0.1:8000/api`  
**Authentication Scheme:** Token Authentication (`Authorization: Token <key>`)

---

## 1. Authentication Endpoints

### 1.1 Register Student
- **Endpoint:** `POST /api/auth/register/`
- **Permissions:** Unauthenticated (`AllowAny`)
- **Request Body:**
```json
{
  "username": "deepak_cse",
  "email": "deepak@example.com",
  "first_name": "Deepak",
  "last_name": "Kumar",
  "branch": "CSE",
  "college_name": "VTU Engineering College",
  "password": "StrongPassword123!"
}
```
- **Response (201 Created):**
```json
{
  "status": "success",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "deepak_cse",
    "email": "deepak@example.com",
    "first_name": "Deepak",
    "profile": {
      "branch": "CSE",
      "college_name": "VTU Engineering College"
    }
  }
}
```

### 1.2 Login
- **Endpoint:** `POST /api/auth/login/`
- **Request Body:** `{"username": "deepak_cse", "password": "StrongPassword123!"}`
- **Response (200 OK):** `{"status": "success", "token": "...", "user": {...}}`

### 1.3 Logout
- **Endpoint:** `POST /api/auth/logout/`
- **Permissions:** `IsAuthenticated`
- **Response (200 OK):** `{"status": "success", "message": "Logged out successfully."}`

---

## 2. Curriculum & Questions Endpoints

### 2.1 List Subjects
- **Endpoint:** `GET /api/subjects/`
- **Response:** List of subjects with target question counts and topics.

### 2.2 List Questions (Filtered)
- **Endpoint:** `GET /api/questions/?subject=python&difficulty=medium&search=generator&page=1`
- **Query Parameters:**
  - `subject`: Subject slug (e.g., `python`, `sql`, `dsa`)
  - `difficulty`: `easy`, `medium`, or `difficult`
  - `search`: Keyword string
  - `limit`: Number of questions
- **Response:** Paginated question objects including options, correct answers, code examples, and interview tips.

---

## 3. Mock Test Simulator Endpoints

### 3.1 Generate Mock Test
- **Endpoint:** `POST /api/mock-tests/generate/`
- **Request Body:** `{"subject": "python", "difficulty": "medium", "question_count": 15}`
- **Response:** Question list with correct answers stripped to preserve test integrity.

### 3.2 Submit Mock Test
- **Endpoint:** `POST /api/mock-tests/submit/`
- **Request Body:**
```json
{
  "subject": "python",
  "answers": {
    "1": "B",
    "2": "A"
  },
  "time_taken_seconds": 450
}
```
- **Response:**
```json
{
  "status": "success",
  "subject": "python",
  "total_questions": 15,
  "correct_count": 12,
  "incorrect_count": 3,
  "score_percentage": 80.0,
  "time_taken_seconds": 450,
  "questions": [...]
}
```

---

## 4. Student Dashboard & Progress Endpoints

### 4.1 Dashboard Overview
- **Endpoint:** `GET /api/dashboard/`
- **Permissions:** `IsAuthenticated`
- **Response:** Real-time aggregated statistics: questions attempted, accuracy percentage, mock tests completed, learning streak, difficulty distribution, and recent activities.

### 4.2 Bookmarks
- **Endpoints:**
  - `GET /api/bookmarks/` — List saved questions
  - `POST /api/bookmarks/` — `{"question": <id>}`
  - `DELETE /api/bookmarks/<id>/` — Remove bookmark

