import unittest
from studyforge.validators import ValidationError,integer,number,date,color,choice,text

class ValidationTests(unittest.TestCase):
    def test_dates(self):
        self.assertEqual(date('2026-11-19','date'),'2026-11-19')
        with self.assertRaises(ValidationError):date('2026-02-31','date')
    def test_boolean_rejected_as_integer(self):
        with self.assertRaises(ValidationError):integer(True,'minutes',1,100)
    def test_ranges(self):
        with self.assertRaises(ValidationError):number(101,'score',0,100)
    def test_colors(self):
        self.assertEqual(color('#112233'),'#112233')
        with self.assertRaises(ValidationError):color('red')
    def test_empty_text(self):
        with self.assertRaises(ValidationError):text('   ','title')

if __name__=='__main__':unittest.main()
