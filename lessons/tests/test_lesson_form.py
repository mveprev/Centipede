from django import forms
from django.urls import reverse
from django.test import TestCase
from lessons.forms import LessonForm
from lessons.models import User, Children, TermDates
from datetime import date

class LessonFormTestCase(TestCase):
    '''Unit tests of the Lesson form'''

    def setUp(self):
        self.url = reverse('student_booking')
        self.user = User.objects.create_user(
            email = 'john.doe@example.org',
            first_name='John',
            last_name = 'Doe',
            password = 'Password123',
        )
        term = TermDates.objects.create(
            name="Term 1",
            start_date=date(2022, 12, 1),
            end_date=date(2022, 12, 12),
        )
        valid_term_pk = TermDates.objects.all()[0].pk
        children = Children.objects.create(
            first_name='Alice',
            last_name='Doe',
            age=5,
            parent=self.user
        )
        valid_children_pk = Children.objects.filter(parent=self.user)[0].pk
        self.form_input = {
            'term': str(valid_term_pk),
            'children': str(valid_children_pk),
            'mondayMorning':True,
            'lessons':1,
            'desiredInterval':7,
            'duration':30,
            'furtherInfo':'I want to learn piano'
        }

    def test_lesson_form_has_necessary_fields(self):
        self.client.login(email='john.doe@example.org', password='Password123')
        request = self.client.get(self.url)
        request.user = self.user
        form = LessonForm(request=request)
        self.assertIn('term', form.fields)
        term_widget=form.fields['term'].widget
        self.assertTrue(isinstance(term_widget, forms.Select))
        self.assertIn('children', form.fields)
        children_widget=form.fields['children'].widget
        self.assertTrue(isinstance(children_widget, forms.Select))
        self.assertIn('mondayMorning', form.fields)
        self.assertIn('mondayAfternoon', form.fields)
        self.assertIn('mondayNight', form.fields)
        self.assertIn('tuesdayMorning', form.fields)
        self.assertIn('tuesdayAfternoon', form.fields)
        self.assertIn('tuesdayNight', form.fields)
        self.assertIn('wednesdayMorning', form.fields)
        self.assertIn('wednesdayAfternoon', form.fields)
        self.assertIn('wednesdayNight', form.fields)
        self.assertIn('thursdayMorning', form.fields)
        self.assertIn('thursdayAfternoon', form.fields)
        self.assertIn('thursdayNight', form.fields)
        self.assertIn('fridayMorning', form.fields)
        self.assertIn('fridayAfternoon', form.fields)
        self.assertIn('fridayNight', form.fields)
        self.assertIn('lessons', form.fields)
        self.assertIn('desiredInterval', form.fields)
        interval_widget=form.fields['desiredInterval'].widget
        self.assertTrue(isinstance(interval_widget, forms.Select))
        self.assertIn('duration', form.fields)
        duration_widget=form.fields['duration'].widget
        self.assertTrue(isinstance(duration_widget, forms.Select))
        self.assertIn('furtherInfo', form.fields)
        info_widget=form.fields['furtherInfo'].widget
        self.assertTrue(isinstance(info_widget, forms.Textarea))

    def test_lesson_form_accepts_valid_input(self):
        self.client.login(email='john.doe@example.org', password='Password123')
        request = self.client.get(self.url)
        request.user = self.user
        form = LessonForm(data = self.form_input, request=request)
        self.assertTrue(form.is_valid())

    def test_student_negative_number_of_lessons(self):
        self.client.login(email='john.doe@example.org', password='Password123')
        request = self.client.get(self.url)
        request.user = self.user
        self.form_input['lessons']=-1
        form = LessonForm(data = self.form_input, request=request)
        self.assertFalse(form.is_valid())

    def test_too_many_lessons_for_term_length(self):
        self.client.login(email='john.doe@example.org', password='Password123')
        request = self.client.get(self.url)
        request.user = self.user
        self.form_input['lessons']=10
        form = LessonForm(data = self.form_input, request=request)
        self.assertFalse(form.is_valid())

    def test_term_has_ended(self):
        self.client.login(email='john.doe@example.org', password='Password123')
        request = self.client.get(self.url)
        request.user = self.user
        term = TermDates.objects.create(
            name="Term 0",
            start_date=date(2022, 11, 1),
            end_date=date(2022, 11, 30),
        )
        self.form_input['term']=term
        form = LessonForm(data = self.form_input, request=request)
        self.assertFalse(form.is_valid())
