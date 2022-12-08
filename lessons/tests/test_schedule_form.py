from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from lessons.forms import ScheduleForm
from lessons.models import User

class ScheduleFormTestCase(TestCase):
    '''Unit tests of the schedule form'''

    def setUp(self):
        self.url = reverse('book_lesson')
        self.user = User.objects.create_superuser(
            first_name='John',
            last_name = 'Doe',
            email = 'john.doe@example.org',
            password = 'Password123'
        )
        self.form_input = {
            'lessons': '1',
            'availability': '1',
            'desiredInterval': '30',
            'duration': '1',
            'furtherInfo': 'Piano',
            'id': '1'
        }

    def test_valid_booking_form(self):
        form = BookingForm(data = self.form_input)
        self.assertTrue(form.is_valid())
