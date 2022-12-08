from django.test import TestCase, Client
from django.urls import reverse
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment
import datetime
from datetime import time, date, datetime

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.save()
        self.client.login(email=self.email, password=self.password)

        self.teacher = User.objects.create(email='teacher@test.com')
        self.teacher.is_teacher = True
        self.teacher.first_name = 'test'
        self.teacher.last_name = 'test'
        self.teacher.outstanding_balance = 0
        self.teacher.save()


        term = TermDates.objects.create(name='test', start_date='2022-01-01', end_date='2022-12-31')
        term.save()

        lesson = Lesson.objects.create(term=TermDates.objects.first(), lessons = 1, desiredInterval = 7, duration = 30, furtherInfo="I want to learn piano", id = 1, user = user, children = None)
        lesson.save()

        booking = Schedule.objects.create(teacher = self.teacher, lesson=lesson, start_time=time(22,12,00), start_date=date(2022,6,1), interval=7,number_of_lessons=7,duration=45)
        booking.save()

    def test_delete(self):
        response = self.client.get(reverse('invoices', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices.html')