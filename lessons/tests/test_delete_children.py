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

        child = Children.objects.create(first_name='test',last_name='test',age=5,parent_id = 1)
        child.save()

    def test_delete_child(self):
        response = self.client.get(reverse('delete-children', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_children.html')
        self.assertEqual(Children.objects.count(), 0)

    def test_delete_child_without_child_id(self):
        response = self.client.get(reverse('delete-children', args=[None]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_children.html')
        self.assertEqual(Children.objects.count(), 1)
