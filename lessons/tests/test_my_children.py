from django.test import TestCase, Client
from django.urls import reverse
from lessons.forms import LessonForm
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment

#Test for my_children in views.py
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.save()
        self.client.login(email=self.email, password=self.password)
        
        
    def test_my_children(self):
        response = self.client.get(reverse('my_children'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_children.html')