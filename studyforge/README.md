# StudyForge — Academic Command Center

A functional, local-first academic planning web application built with Python's standard library, SQLite and vanilla JavaScript. **No pip installs needed.**

## Features

- **Courses**: add courses, codes, credits, target grades, and colors.
- **Task manager**: deadlines, priorities, completion states, estimated effort, delete tasks.
- **Study log**: log timed sessions, focus ratings, notes and dates.
- **Assessment tracker**: record scored evaluations with weights.
- **Transparent performance projection**: show tentative grade estimates with an uncertainty range, confidence, and data-availability safeguards.
- **Daily planner**: allocates a selected time budget to unfinished work by deadline and priority.
- **Dashboard**: weekly activity, upcoming work, and at-a-glance metrics.
- **SQLite database**: data persists after browser/server restarts.
- **Automated tests**: validators, projections, scheduling and data operations.

## Running on Windows

1. Install Python 3.10+ from python.org (tick **Add Python to PATH**).
2. Extract `StudyForge_Project.zip` and open a PowerShell terminal **in the folder containing the `studyforge` directory**.
3. Run:

   ```powershell
   python -m studyforge.run
   ```

4. Open **http://127.0.0.1:8765** in Chrome.
5. Add a course, then tasks, sessions and assessments. Data saves automatically to `studyforge/studyforge.db`.
6. Stop server with **Ctrl + C**.

On some Windows installations, run `py -m studyforge.run` instead.

## Run tests

```powershell
python -m unittest discover -s studyforge/tests -v
```

## Architecture

- `studyforge/server.py` — HTTP and static file handler
- `studyforge/service.py` — input coordination and dashboard logic
- `studyforge/repository.py` — parameterized database operations
- `studyforge/db.py` — persistence, indexes and schema
- `studyforge/validators.py` — data validation
- `studyforge/predictor.py` — transparent grade heuristic
- `studyforge/planner.py` — daily prioritization
- `studyforge/web/` — responsive HTML, CSS and JS frontend
- `studyforge/tests/` — standard-library unit tests

## Important limitations

The performance projection is a heuristic and **not** a trained machine learning system, official grade forecast, validated statistical model or guaranteed result. Assessment weights are supplied by the user; scores may not be comparable between course grading schemes. Intended for personal planning, not academic decisions. This app has no user authentication and should only be run on localhost; it is **not production-ready for public hosting**.

## Data and privacy

No cloud account, external database or external API is required. The interface optionally requests a Google Fonts stylesheet (falls back to system fonts offline). The SQLite database is local and excluded from version control.

## License

MIT (see LICENSE).
