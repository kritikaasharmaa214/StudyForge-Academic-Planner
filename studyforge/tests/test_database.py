import os
import tempfile
import unittest
from studyforge import db,service

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.old=db.DB_PATH
        db.DB_PATH=os.path.join(self.temp.name,'test.db')
        db.initialize()

    def tearDown(self):
        db.DB_PATH=self.old
        self.temp.cleanup()

    def test_create_and_dashboard(self):
        cid=service.create('courses',{'name':'Computer Networks','code':'CS301'})['id']
        service.create('tasks',{'course_id':cid,'title':'Revise OSI','due_date':'2026-12-05'})
        self.assertEqual(service.dashboard()['tasks_open'],1)

    def test_status(self):
        cid=service.create('courses',{'name':'Data Structures','code':'CS302'})['id']
        tid=service.create('tasks',{'course_id':cid,'title':'Trees','due_date':'2026-12-05'})['id']
        service.update_task(tid,{'status':'done'})
        self.assertEqual(service.dashboard()['tasks_completed'],1)

    def test_cascade(self):
        cid=service.create('courses',{'name':'Mathematics','code':'MTH101'})['id']
        service.create('assessments',{'course_id':cid,'name':'Quiz','score':80,'weight':20})
        service.remove('courses',cid)
        self.assertEqual(len(service.collection('assessments')),0)

    def test_duplicate_course_rejected(self):
        import sqlite3
        service.create('courses',{'name':'Math','code':'MTH101'})
        with self.assertRaises(sqlite3.IntegrityError):service.create('courses',{'name':'Math 2','code':'MTH101'})

if __name__=='__main__':unittest.main()
