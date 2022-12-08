from django import forms
from django.test import TestCase
from lessons.forms import ScheduleForm, CustomScheduleForm
from lessons.models import User, Lesson, Schedule
from lessons.utils import Calendar
from datetime import date, time

class ScheduleFormTestCase(TestCase):
    '''Unit tests of the schedule form'''

    def setUp(self):
        self.user = User.objects.create_user(
            email = 'john.doe@example.org',
            first_name='John',
            last_name = 'Doe',
            password = 'Password123',
        )
        teacher = User.objects.create_user(
            email="dwayne.johnson@example.org",
            password="Password123",
            first_name="Dwayne",
            last_name="Johnson",
            is_teacher=True,
        )
        valid_teacher_pk = User.objects.filter(is_teacher=True)[0].pk
        self.form_input = {
            'teacher': str(valid_teacher_pk),
            'start_time':time(22,12,00),
            'start_date':date(2023, 6, 1),
            'interval':7,
            'number_of_lessons':7,
            'duration': 45
        }
        self.second_form_input = {
            'teacher': str(valid_teacher_pk),
            'start_time':time(23,12,00),
            'start_date':date(2023, 6, 1),
            'interval':7,
            'number_of_lessons':7,
            'duration': 45
        }

    def test_schedule_form_has_necessary_fields(self):
        form = ScheduleForm()
        self.assertIn('teacher', form.fields)
        teacher_widget=form.fields['teacher'].widget
        self.assertTrue(isinstance(teacher_widget, forms.Select))
        self.assertIn('start_time', form.fields)
        start_time_widget=form.fields['start_time'].widget
        self.assertTrue(isinstance(start_time_widget, forms.TimeInput))
        self.assertIn('start_date', form.fields)
        start_date_widget=form.fields['start_date'].widget
        self.assertTrue(isinstance(start_date_widget, forms.DateInput))
        self.assertIn('interval', form.fields)
        interval_widget=form.fields['interval'].widget
        self.assertTrue(isinstance(interval_widget, forms.Select))
        self.assertIn('number_of_lessons', form.fields)
        self.assertIn('duration', form.fields)
        duration_widget=form.fields['duration'].widget
        self.assertTrue(isinstance(duration_widget, forms.Select))

    def test_schedule_form_accepts_valid_input(self):
        form = ScheduleForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_admin_negative_number_of_lessons(self):
        self.form_input['number_of_lessons']=-1
        form = ScheduleForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_teacher_schedules_do_not_overlap(self):
        form = ScheduleForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        lesson = Lesson.objects.create(
            lessons=2,
            desiredInterval=7,
            duration=30,
            furtherInfo="I want to learn piano",
            user=self.user
        )
        newSchedule = form.save(commit=False)
        newSchedule.lesson = lesson
        newSchedule.save()
        second_form = ScheduleForm(data = self.second_form_input)
        self.assertTrue(second_form.is_valid())

    def test_teacher_schedules_overlap(self):
        self.second_form_input['start_time'] =  self.form_input['start_time']
        form = ScheduleForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        lesson = Lesson.objects.create(
            lessons=2,
            desiredInterval=7,
            duration=30,
            furtherInfo="I want to learn piano",
            user=self.user
        )
        newSchedule = form.save(commit=False)
        newSchedule.lesson = lesson
        newSchedule.save()
        second_form = ScheduleForm(data = self.second_form_input)
        self.assertFalse(second_form.is_valid())

    def test_schedule_form_must_save_correctly(self):
        form = ScheduleForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        before_count = Schedule.objects.count()
        lesson = Lesson.objects.create(
            lessons=2,
            desiredInterval=7,
            duration=30,
            furtherInfo="I want to learn piano",
            user=self.user
        )
        newSchedule = form.save(commit=False)
        newSchedule.lesson = lesson
        newSchedule.save()
        after_count = Schedule.objects.count()
        self.assertEqual(after_count, before_count+1)
        schedule = Schedule.objects.get(teacher=newSchedule.teacher)
        self.assertEqual(schedule.lesson, lesson)
        self.assertEqual(schedule.start_time, time(22,12,00))
        self.assertEqual(schedule.start_date, date(2023,6,1))
        self.assertEqual(schedule.interval, 7)
        self.assertEqual(schedule.number_of_lessons, 7)
        self.assertEqual(schedule.duration, 45)

    def test_custom_schedule_form(self):
        form = ScheduleForm(data = self.form_input)
        queryset=User.objects.filter(is_teacher=True)
        customScheduleForm = CustomScheduleForm(queryset=queryset)
        customScheduleForm.label_from_instance(queryset[0])

    def test_calendar_form(self):
        form = ScheduleForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        teacher = User.objects.filter(is_teacher=True)[0]
        calendar = Calendar(teacher, year=2023, month=6)
        lesson = Lesson.objects.create(
            lessons=2,
            desiredInterval=7,
            duration=30,
            furtherInfo="I want to learn piano",
            user=self.user
        )
        schedule = form.save(commit=False)
        schedule.lesson = lesson
        schedule.save()
        second_form = ScheduleForm(data = self.second_form_input)
        second_schedule = form.save(commit=False)
        second_schedule.lesson = lesson
        second_schedule.save()
        calendar.formatday(1, Schedule.objects)
        calendar.formatday(0, Schedule.objects)
        calendar.formatmonth(withyear=True)
