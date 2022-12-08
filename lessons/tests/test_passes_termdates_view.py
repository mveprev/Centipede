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

    def test_termdates(self):
        response = self.client.get(reverse('term_dates'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_dates.html')

    def test_termdates_post(self):
        response = self.client.post(reverse('term_dates'),{
        'name':'test',
        'start_date':date(2022,1,1),
        'end_date':date(2022,1,20),
        })
        self.assertEquals(response.status_code, 302)
