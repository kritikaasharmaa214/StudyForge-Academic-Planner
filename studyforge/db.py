"""SQLite persistence and schema for StudyForge."""
import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get('STUDYFORGE_DB', os.path.join(os.path.dirname(__file__), 'studyforge.db'))

SCHEMA = '''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS courses (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 code TEXT NOT NULL UNIQUE,
 credits INTEGER NOT NULL DEFAULT 3 CHECK(credits BETWEEN 1 AND 8),
 target_grade REAL NOT NULL DEFAULT 85 CHECK(target_grade BETWEEN 0 AND 100),
 color TEXT NOT NULL DEFAULT '#6275ee',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS tasks (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
 title TEXT NOT NULL,
 due_date TEXT NOT NULL,
 priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low','medium','high')),
 estimated_minutes INTEGER NOT NULL DEFAULT 60 CHECK(estimated_minutes BETWEEN 5 AND 1440),
 status TEXT NOT NULL DEFAULT 'todo' CHECK(status IN ('todo','doing','done')),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS sessions (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
 minutes INTEGER NOT NULL CHECK(minutes BETWEEN 1 AND 1440),
 focus_score INTEGER NOT NULL CHECK(focus_score BETWEEN 1 AND 5),
 studied_on TEXT NOT NULL,
 notes TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS assessments (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
 name TEXT NOT NULL,
 score REAL NOT NULL CHECK(score BETWEEN 0 AND 100),
 weight REAL NOT NULL CHECK(weight > 0 AND weight <= 100),
 assessed_on TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS tasks_due_idx ON tasks(due_date, status);
CREATE INDEX IF NOT EXISTS sessions_course_day_idx ON sessions(course_id, studied_on);
CREATE INDEX IF NOT EXISTS assessments_course_idx ON assessments(course_id);
'''

@contextmanager
def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def initialize():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    with connect() as db:
        db.executescript(SCHEMA)

def rows(query, params=()):
    with connect() as db:
        return [dict(r) for r in db.execute(query, params).fetchall()]

def execute(query, params=()):
    with connect() as db:
        cursor = db.execute(query, params)
        return cursor.lastrowid, cursor.rowcount
