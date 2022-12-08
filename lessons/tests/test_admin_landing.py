from django.test import TestCase, Client
from django.urls import reverse

#Test for admin_landing_page in views.py
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        self.admin = True
        user = User.objects.create(email=self.email)
        user.is_staff = True
        user.set_password(self.password)
        user.save()
        self.client.login(email=self.email, password=self.password)


    def test_admin_landing_page(self):
        response = client.get(reverse('admin_landing_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_landing_page.html')


    def test_admin_lesson_page(self):
        response = client.get(reverse('admin_lessons'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_lessons.html')

    def test_admin_payment(self):
        response = client.get(reverse('admin_payment'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_payment.html')

    def test_view_term_dates(self):
        response = client.get(reverse('view_term_dates'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_term_dates.html')
