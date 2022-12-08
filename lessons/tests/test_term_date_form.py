from django.test import TestCase
from lessons.models import TermDates
from lessons.forms import DateForm
from datetime import date

class TermDateFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'name':'Term 0',
            'start_date': date(2003, 4, 1),
            'end_date': date(2003, 4, 14),
        }
        self.second_form_input  = {
            'name':'Term 1',
            'start_date': date(2003, 4, 15),
            'end_date': date(2003, 4, 30),
        }

    def test_valid_term_date(self):
        form = DateForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = DateForm()
        self.assertIn('start_date', form.fields)
        self.assertIn('end_date', form.fields)

    def test_range_is_not_valid(self):
        self.form_input['end_date'] = date(2003, 4, 1)
        form = DateForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_terms_do_not_overlap(self):
        form = DateForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        form.save()
        second_form = DateForm(data = self.second_form_input)
        self.assertTrue(second_form.is_valid())

    def test_term_end_and_start_dates_overlap(self):
        self.second_form_input['start_date'] =  self.form_input['end_date']
        form = DateForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        form.save()
        second_form = DateForm(data = self.second_form_input)
        self.assertFalse(second_form.is_valid())

    def test_term_start_and_end_dates_overlap(self):
        self.form_input['end_date'] =  self.second_form_input['start_date']
        second_form = DateForm(data = self.second_form_input)
        self.assertTrue(second_form.is_valid())
        second_form.save()
        form = DateForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_term_has_no_start_date_selected(self):
        self.form_input['start_date'] = None
        form = DateForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_term_has_no_end_date_selected(self):
        self.form_input['end_date'] =  None
        form = DateForm(data = self.form_input)
        self.assertFalse(form.is_valid())
