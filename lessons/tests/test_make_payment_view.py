from django.test import TestCase, Client
from django.urls import reverse
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.is_staff=True
        user.save()
        self.client.login(email=self.email, password=self.password)

    def test_make_payment(self):
        response = self.client.get(reverse('make_payment', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'make_payment.html')

    def test_make_payment_post(self):
        response = self.client.post(reverse('make_payment', args=[1]),{
            'amount_paid':100
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_payment.html')