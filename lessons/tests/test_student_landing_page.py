from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_student_landing_page(self):
        response = self.client.get(reverse('student_landing_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_landing_page.html')