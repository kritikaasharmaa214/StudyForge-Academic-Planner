"""Study scheduling: prioritize overdue and high-priority tasks without hiding estimates."""
from datetime import date

PRIORITY = {'high':3,'medium':2,'low':1}

def rank_tasks(tasks, today=None):
    today = today or date.today()
    def key(t):
        due = date.fromisoformat(t['due_date'])
        days = (due-today).days
        return (t['status']=='done', days, -PRIORITY[t['priority']],t['id'])
    return sorted(tasks, key=key)

def daily_plan(tasks, available_minutes=120, today=None):
    if not 15 <= available_minutes <= 720:
        raise ValueError('available_minutes must be between 15 and 720')
    today = today or date.today()
    plan=[]; remaining=available_minutes
    for task in rank_tasks(tasks,today):
        if task['status']=='done' or remaining<=0: continue
        allocated=min(task['estimated_minutes'], remaining)
        if allocated < 5: break
        plan.append({'task_id':task['id'],'title':task['title'],'course_id':task['course_id'],
                     'due_date':task['due_date'],'priority':task['priority'],'minutes':allocated,
                     'overdue':task['due_date']<today.isoformat()})
        remaining-=allocated
    return {'items':plan,'allocated_minutes':available_minutes-remaining,
            'free_minutes':remaining,'available_minutes':available_minutes}
