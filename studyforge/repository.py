"""Parameterized SQL operations and aggregate queries."""
import sqlite3
from . import db

class NotFound(Exception):
    pass

def list_courses():
    return db.rows('SELECT * FROM courses ORDER BY name')

def ensure_course(cid):
    if not db.rows('SELECT id FROM courses WHERE id=?',(cid,)):
        raise NotFound('Course not found')

def add_course(data):
    return db.execute('INSERT INTO courses(name,code,credits,target_grade,color) VALUES(?,?,?,?,?)',data)[0]

def add_task(data):
    return db.execute('INSERT INTO tasks(course_id,title,due_date,priority,estimated_minutes) VALUES(?,?,?,?,?)',data)[0]

def list_tasks():
    return db.rows('SELECT tasks.*, courses.name AS course_name, courses.color AS course_color FROM tasks JOIN courses ON courses.id=tasks.course_id ORDER BY tasks.due_date, tasks.id')

def change_task(task_id,status):
    _,count=db.execute('UPDATE tasks SET status=? WHERE id=?',(status,task_id))
    if not count: raise NotFound('Task not found')

def delete_task(task_id):
    _,count=db.execute('DELETE FROM tasks WHERE id=?',(task_id,))
    if not count: raise NotFound('Task not found')


def add_session(data, task_id=None):
    course_id, minutes, focus_score, studied_on, notes = data

    if task_id is not None:
        task = db.rows(
            'SELECT course_id FROM tasks WHERE id=?',
            (task_id,)
        )
        if not task:
            raise NotFound('Task not found')
        if task[0]['course_id'] != course_id:
            raise ValueError('Task does not belong to the selected course')

    return db.execute(
        '''INSERT INTO sessions
        (course_id, minutes, focus_score, studied_on, notes, task_id)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (course_id, minutes, focus_score, studied_on, notes, task_id)
    )[0]

def list_sessions():
    return db.rows('SELECT sessions.*, courses.name AS course_name FROM sessions JOIN courses ON courses.id=sessions.course_id ORDER BY studied_on DESC,id DESC')

def add_assessment(data):
    return db.execute('INSERT INTO assessments(course_id,name,score,weight,assessed_on) VALUES(?,?,?,?,?)',data)[0]

def list_assessments():
    return db.rows('SELECT assessments.*, courses.name AS course_name FROM assessments JOIN courses ON courses.id=assessments.course_id ORDER BY assessed_on DESC,id DESC')

def delete_course(cid):
    _,count=db.execute('DELETE FROM courses WHERE id=?',(cid,))
    if not count: raise NotFound('Course not found')

def task_progress(task_id):
    task = db.rows(
        'SELECT id, title, estimated_minutes, status FROM tasks WHERE id=?',
        (task_id,)
    )
    if not task:
        raise NotFound('Task not found')

    studied = db.rows(
        '''SELECT COALESCE(SUM(minutes), 0) AS total
           FROM sessions WHERE task_id=?''',
        (task_id,)
    )[0]['total']

    estimated = task[0]['estimated_minutes']

    return {
        'task_id': task_id,
        'title': task[0]['title'],
        'estimated_minutes': estimated,
        'completed_minutes': studied,
        'remaining_minutes': 0 if task[0]['status'] == 'done'
                             else max(0, estimated - studied),
        'progress_percent': min(100, round(studied / estimated * 100, 1))
    }
