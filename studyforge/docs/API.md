# StudyForge API

Local-only JSON HTTP API at http://127.0.0.1:8765/api/. All writes accept Content-Type: application/json.

## Collections

- `GET /api/courses` — list courses
- `POST /api/courses` — `{ "name": "Data Structures", "code": "CSE301", "credits": 4, "target_grade": 85, "color": "#6275ee" }`
- `DELETE /api/courses/<id>` — delete a course and its related records
- `GET /api/tasks` — list tasks, including joined course metadata
- `POST /api/tasks` — `{ "course_id": 1, "title": "Revise graphs", "due_date": "2026-12-01", "priority": "high", "estimated_minutes": 90 }`
- `PATCH /api/tasks/<id>` — `{ "status": "doing" }` or `todo`/`done`
- `DELETE /api/tasks/<id>` — delete one task
- `GET /api/sessions` — list study sessions
- `POST /api/sessions` — `{ "course_id": 1, "minutes": 60, "focus_score": 4, "studied_on": "2026-11-19", "notes": "Trees" }`
- `GET /api/assessments` — list graded events
- `POST /api/assessments` — `{ "course_id": 1, "name": "Midterm", "score": 82, "weight": 20, "assessed_on": "2026-11-19" }`
- `GET /api/dashboard` — counts, weekly study activity, projections, upcoming work
- `GET /api/plan?minutes=120` — a prioritised list fitting a study time budget

## HTTP statuses

`200`: successful read/update/delete; `201`: created; `400`: validation error; `404`: missing route or record; `405`: unsupported method; `409`: uniqueness or relational constraint violation.

## Data integrity

All SQL uses parameterized placeholders; foreign keys are enforced and parent course deletion cascades to child records. The application currently has no authentication or user isolation. Avoid binding the server to a public network interface.
