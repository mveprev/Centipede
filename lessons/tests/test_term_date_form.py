from django.test import TestCase
from lessons.models import TermDates
from lessons.forms import DateForm

class TermDateFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'start_date': '04/1/2003',
            'end_date': '04/14/2003'
        }
        self.second_form_input  = {
            'start_date': '04/15/2003',
            'end_date': '04/30/2003'
        }
    
    def test_valid_term_date(self):
        form = DateForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_form_has_necessary_fields(self):
        form = DateForm()
        self.assertIn('start_date', form.fields)
        self.assertIn('end_date', form.fields)

    def test_range_is_valid(self):
        self.form_input['end_date'] = '04/01/2003'
        form = DateForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_range_is_valid_again(self):
        self.form_input['end_date'] = '04/01/2003'
        form = DateForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_terms_do_not_overlap(self):
        self.second_form_input['start_date'] =  self.form_input['end_date']
        form = DateForm(data = self.form_input)
        second_form = DateForm(data = self.second_form_input)
        self.assertFalse(form.is_valid())
        self.assertFalse(second_form.is_valid())
        