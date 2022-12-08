from django.test import TestCase, Client
from django.urls import reverse
from lessons.forms import LessonForm
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment
from datetime import time, date

#Test for reject_booking in views.py
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        self.admin = True
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.is_staff = True
        user.save()
        self.client.login(email=self.email, password=self.password)

        term = TermDates.objects.create(name = 'test', start_date='2022-01-01', end_date='2022-12-31')
        term.save()

        lesson = Lesson.objects.create(term=TermDates.objects.first(), lessons = 1, desiredInterval = 7, duration = 30, id = 1, user_id = 1, children = None)
        lesson.save()

        self.teacher = User.objects.create(email='teacher@test.com')
        self.teacher.first_name = 'test'
        self.teacher.last_name = 'test'
        self.teacher.outstanding_balance = 0
        self.teacher.is_teacher = True
        self.teacher.save()

        booking = Schedule.objects.create(teacher = self.teacher, lesson=lesson, start_time=time(22,12,00), start_date=date(2022,6,1), interval=7,number_of_lessons=7,duration=45)
        booking.save()

    def test_delete_scheduele(self):
        response = self.client.get(reverse('delete-booking', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Lesson.objects.count(), 0)
        self.assertEqual(Schedule.objects.count(), 0)
        self.assertTemplateUsed(response, 'admin_lessons.html')

    def test_delete_second_schedule(self):
        second_lesson = Lesson.objects.create(term=TermDates.objects.first(), lessons = 1, desiredInterval = 7, duration = 45, id = 2, user_id = 1, children = None)
        second_booking = Schedule.objects.create(teacher = self.teacher, lesson=second_lesson, start_time=time(23,12,00), start_date=date(2022,6,1), interval=7,number_of_lessons=7,duration=45)
        second_booking.save()
        response = self.client.get(reverse('delete-booking', args=[2]))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertTemplateUsed(response, 'admin_lessons.html')

    def test_delete_third_schedule(self):
        third_lesson = Lesson.objects.create(term=TermDates.objects.first(), lessons = 1, desiredInterval = 7, duration = 60, id = 3, user_id = 1, children = None)
        third_booking = Schedule.objects.create(teacher = self.teacher, lesson=third_lesson, start_time=time(23,12,00), start_date=date(2022,6,1), interval=7,number_of_lessons=7,duration=60)
        third_booking.save()
        response = self.client.get(reverse('delete-booking', args=[3]))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertTemplateUsed(response, 'admin_lessons.html')

    def test_delete_schedule_without_lesson_id(self):
        fourth_lesson = Lesson.objects.create(term=TermDates.objects.first(), lessons = 1, desiredInterval = 7, duration = 60, id = 4, user_id = 1, children = None)
        fourth_booking = Schedule.objects.create(teacher = self.teacher, lesson=fourth_lesson, start_time=time(23,12,00), start_date=date(2022,6,1), interval=7,number_of_lessons=7,duration=60)
        fourth_booking.save()
        response = self.client.get(reverse('delete-booking', args=[None]))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Schedule.objects.count(), 2)
        self.assertTemplateUsed(response, 'admin_lessons.html')
