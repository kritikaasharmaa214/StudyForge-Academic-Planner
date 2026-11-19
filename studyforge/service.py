"""API business logic. Designed to work with any HTTP frontend."""
from datetime import date
from . import repository as repo
from . import validators as v
from . import predictor, planner

def collection(name):
    if name=='courses': return repo.list_courses()
    if name=='tasks': return planner.rank_tasks(repo.list_tasks())
    if name=='sessions': return repo.list_sessions()
    if name=='assessments': return repo.list_assessments()
    raise repo.NotFound('Unknown resource')

def create(name, payload):
    p=v.mapping(payload)
    if name=='courses':
        code=v.text(p.get('code'),'code',15).upper()
        name_txt=v.text(p.get('name'),'name',80)
        data=(name_txt,code,v.integer(p.get('credits',3),'credits',1,8),
              v.number(p.get('target_grade',85),'target_grade',0,100),v.color(p.get('color','#6275ee')))
        return {'id':repo.add_course(data)}
    if name=='tasks':
        cid=v.integer(p.get('course_id'),'course_id',1,99999999);repo.ensure_course(cid)
        data=(cid,v.text(p.get('title'),'title',160),v.date(p.get('due_date'),'due_date'),
              v.choice(p.get('priority','medium'),'priority',('low','medium','high')),
              v.integer(p.get('estimated_minutes',60),'estimated_minutes',5,1440))
        return {'id':repo.add_task(data)}
    if name=='sessions':
        cid=v.integer(p.get('course_id'),'course_id',1,99999999);repo.ensure_course(cid)
        data=(cid,v.integer(p.get('minutes'),'minutes',1,1440),
              v.integer(p.get('focus_score',3),'focus_score',1,5),
              v.date(p.get('studied_on',date.today().isoformat()),'studied_on'),
              str(p.get('notes',''))[:500])
        return {'id':repo.add_session(data)}
    if name=='assessments':
        cid=v.integer(p.get('course_id'),'course_id',1,99999999);repo.ensure_course(cid)
        data=(cid,v.text(p.get('name'),'name',100),v.number(p.get('score'),'score',0,100),
              v.number(p.get('weight'),'weight',0.001,100),
              v.date(p.get('assessed_on',date.today().isoformat()),'assessed_on'))
        return {'id':repo.add_assessment(data)}
    raise repo.NotFound('Unknown resource')

def dashboard():
    courses=repo.list_courses();tasks=repo.list_tasks();sessions=repo.list_sessions();assessments=repo.list_assessments()
    projections=[]
    for c in courses:
        p=predictor.project([a for a in assessments if a['course_id']==c['id']],
                            [s for s in sessions if s['course_id']==c['id']],
                            [t for t in tasks if t['course_id']==c['id']], c['target_grade'])
        projections.append({'course':c, 'projection':p})
    return {'courses':len(courses),'tasks_open':sum(t['status']!='done' for t in tasks),
            'tasks_completed':sum(t['status']=='done' for t in tasks),
            'study_minutes':sum(s['minutes'] for s in sessions),
            'weekly':predictor.weekly_minutes(sessions),
            'projections':projections,'upcoming':planner.rank_tasks(tasks)[:8]}

def plan(minutes):
    return planner.daily_plan(repo.list_tasks(),v.integer(minutes,'minutes',15,720))

def update_task(task_id,p):
    repo.change_task(v.integer(task_id,'id',1,99999999),v.choice(p.get('status'),'status',('todo','doing','done')))
    return {'updated':True}

def remove(name,resource_id):
    rid=v.integer(resource_id,'id',1,99999999)
    if name=='tasks':repo.delete_task(rid)
    elif name=='courses':repo.delete_course(rid)
    else:raise repo.NotFound('Unknown resource')
    return {'deleted':True}
