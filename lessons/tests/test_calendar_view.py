from django.test import TestCase
from datetime import time, date
from lessons.views import prev_month, next_month, get_date

class TestViews(TestCase):
        
    def test_prev_month(self):
        prev = prev_month(date(2022, 6, 1))
        should = 'month=2022-5'
        self.assertEquals(prev, should)
    
    def test_next_month(self):
        nex = next_month(date(2022,6,1))
        should = 'month=2022-7'
        self.assertEquals(nex, should)

    def test_get_date(self):
        datex = get_date('2022-1')
        should = date(2022,1,1)
        self.assertTrue(datex==should)

    
   
