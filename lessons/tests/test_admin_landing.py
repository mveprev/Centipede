from django.test import TestCase, Client
from django.urls import reverse

#Test for admin_landing_page in views.py
class TestViews(TestCase):
    def test_admin_landing_page(self):
        client = Client()
        response = client.get(reverse('admin_landing_page'))
        self.assertEquals(response.status_code, 302)
    
    def test_admin_lesson_page(self):
        client = Client()
        response = client.get(reverse('admin_lessons'))
        self.assertEquals(response.status_code, 302)
        
    def test_admin_payment(self):
        client = Client()
        response = client.get(reverse('admin_payment'))
        self.assertEquals(response.status_code, 302)
        
    def test_view_term_dates(self):
        client = Client()
        response = client.get(reverse('view_term_dates'))
        self.assertEquals(response.status_code, 302)