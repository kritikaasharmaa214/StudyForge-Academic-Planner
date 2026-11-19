import unittest
from datetime import date
from studyforge.planner import daily_plan,rank_tasks

class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.tasks=[{'id':1,'title':'later','course_id':2,'due_date':'2026-12-02','priority':'high','estimated_minutes':100,'status':'todo'},
                    {'id':2,'title':'urgent','course_id':1,'due_date':'2026-11-18','priority':'low','estimated_minutes':45,'status':'todo'},
                    {'id':3,'title':'done','course_id':1,'due_date':'2026-11-17','priority':'high','estimated_minutes':60,'status':'done'}]
    def test_overdue_first(self):
        self.assertEqual(rank_tasks(self.tasks,date(2026,11,19))[0]['id'],2)
    def test_completed_excluded(self):
        a=daily_plan(self.tasks,60,date(2026,11,19))
        self.assertEqual([x['task_id'] for x in a['items']],[2,1])
        self.assertEqual(a['allocated_minutes'],60)
    def test_bad_budget(self):
        with self.assertRaises(ValueError):daily_plan(self.tasks,0)

if __name__=='__main__':unittest.main()
