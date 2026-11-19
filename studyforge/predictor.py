"""Transparent heuristic projection, not a trained machine-learning model."""
from datetime import date, timedelta

GRADE_BANDS = [(90,'A+'),(80,'A'),(70,'B'),(60,'C'),(50,'D'),(0,'F')]

def grade_label(score):
    for threshold, label in GRADE_BANDS:
        if score >= threshold:
            return label
    return 'F'

def project(assessments, sessions, pending_tasks, target_grade=85):
    """Estimate a range by weighted assessments and engagement, with explicit uncertainty.

    If there are no assessments, a numerical estimate is deliberately omitted.
    Sessions contribute context only; no causal claim or reliable ML inference is made.
    """
    total_weight = sum(float(a['weight']) for a in assessments)
    if not assessments or total_weight <= 0:
        return {'estimate': None, 'lower': None, 'upper': None,
                'label': 'Not enough graded data', 'confidence': 'insufficient',
                'reason': 'Add a scored assessment to see a tentative projection.',
                'observed_weight': 0, 'study_hours': round(sum(s['minutes'] for s in sessions)/60,1)}
    observed = sum(float(a['score'])*float(a['weight']) for a in assessments) / total_weight
    study_hours = sum(int(s['minutes']) for s in sessions) / 60
    avg_focus = sum(int(s['focus_score']) for s in sessions)/len(sessions) if sessions else 3
    overdue = sum(1 for t in pending_tasks if t['status'] != 'done' and t['due_date'] < date.today().isoformat())
    # A small heuristic adjustment, capped, never presented as a statistically validated forecast.
    engagement = max(-4, min(4, (study_hours/8 - 1)*1.2 + (avg_focus-3)*0.7 - overdue*0.75))
    estimate = round(max(0, min(100, observed + engagement)), 1)
    uncertainty = 5 if total_weight >= 50 else (9 if total_weight >= 25 else 14)
    return {'estimate': estimate, 'lower': round(max(0,estimate-uncertainty),1),
            'upper': round(min(100,estimate+uncertainty),1), 'label': grade_label(estimate),
            'confidence': 'moderate' if total_weight >= 50 else 'low',
            'reason': 'Heuristic based on weighted recorded marks, recent study effort and overdue tasks; not a validated prediction.',
            'observed_weight': round(total_weight,1),'study_hours': round(study_hours,1),
            'target_gap': round(target_grade-estimate,1)}

def weekly_minutes(sessions, days=7, today=None):
    today = today or date.today()
    lookup = {}
    for s in sessions:
        lookup[s['studied_on']] = lookup.get(s['studied_on'],0)+s['minutes']
    return [{'date': (today-timedelta(days=i)).isoformat(),
             'minutes': lookup.get((today-timedelta(days=i)).isoformat(),0)}
            for i in reversed(range(days))]
