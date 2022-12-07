from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from lessons.forms import LessonForm
from lessons.models import User, Children

class LessonFormTestCase(TestCase):
    '''Unit tests of the Lesson form'''

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.create_user(
            first_name='John',
            last_name = 'Doe',
            email = 'john.doe@example.org',
            password = 'Password123'
        )
        self.children = Children.objects.create_user(
            first_name = 'Jane',
            last_name = 'Doe',
            age = '10',
            email = 'jane.doe@example.org',
            id = '',
            parent = ''
        )
        self.form_input = {
            'children': ,
            'lessons': ,
            'availability': ,
            'desiredInterval': ,
            'duration': ,
            'furtherInfo': ,
            'id':
        }

    def test_valid_lesson_form(self):
        form = LessonForm(data = self.form_input)
        self.assertTrue(form.is_valid())
