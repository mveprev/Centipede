from django.test import TestCase
from django.urls import reverse
from lessons.models import Student
from .helpers import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('log_out')
        self.user = Student.objects.create_user(
            email = 'james@example.org',
            first_name='James',
            last_name = 'Lu',
            password = 'Lu123',
        )

    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')

    def test_get_log_out(self):
        self.client.login(email='james@example.org', password='Lu123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(self._is_logged_in())
