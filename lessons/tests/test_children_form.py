from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from lessons.forms import LessonForm
from lessons.models import User

class ChildrenFormTestCase(TestCase):
    '''Unit tests of the children form'''

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.create_user(
            first_name='John',
            last_name = 'Doe',
            email = 'john.doe@example.org',
            password = 'Password123'
        )
        self.form_input = {
            'first_name' : 'James',
            'last_name' : 'Lu',
            'email' : 'james@example.org',
            'new_password' : 'Lu123',
            'password_confirmation' : 'Lu123'
        }

    def test_valid_lesson_form(self):
        form = LessonForm(data = self.form_input)
        self.assertTrue(form.is_valid())
