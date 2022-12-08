from django.test import TestCase
import datetime
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

    # def test_get_date(self):
    #     date = get_date('2022-1').days
    #     should = date(2022,1,1).days
    #     self.assertEquals(date,should)


    
   
