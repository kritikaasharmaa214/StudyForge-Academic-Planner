import unittest
from datetime import date
from studyforge.predictor import project,grade_label,weekly_minutes

class PredictorTests(unittest.TestCase):
    def test_no_assessments_does_not_invent_score(self):
        p=project([],[],[])
        self.assertIsNone(p['estimate'])
        self.assertEqual(p['confidence'],'insufficient')

    def test_weighted_marks(self):
        a=[{'score':60,'weight':20},{'score':90,'weight':30}]
        p=project(a,[],[])
        self.assertAlmostEqual(p['estimate'],76.8)
        self.assertEqual(p['observed_weight'],50)

    def test_bounds(self):
        p=project([{'score':100,'weight':100}],[],[])
        self.assertLessEqual(p['upper'],100)
        self.assertGreaterEqual(p['lower'],0)

    def test_grades(self):
        self.assertEqual(grade_label(90),'A+')
        self.assertEqual(grade_label(59),'D')

    def test_weekly_chart(self):
        s=[{'studied_on':'2026-11-19','minutes':20},{'studied_on':'2026-11-19','minutes':35}]
        a=weekly_minutes(s,days=1,today=date(2026,11,19))
        self.assertEqual(a[0]['minutes'],55)

if __name__=='__main__':unittest.main()
