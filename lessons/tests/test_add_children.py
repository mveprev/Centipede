from django.test import TestCase, Client
from django.urls import reverse
from lessons.forms import LessonForm
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment

#Test for add_children in views.py
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.save()
        self.client.login(email=self.email, password=self.password)
        
    def test_add_children_get(self):
        response = self.client.get(reverse('add_children'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_children.html')
        
    def test_add_children_post(self):
        response = self.client.post(reverse('add_children'), {
            'first_name':'test',
            'last_name':'test',
            'age':5
        })
        self.assertEquals(response.status_code, 302)
        self.assertEqual(Children.objects.count(), 1)
        
        