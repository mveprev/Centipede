from django.test import TestCase, Client
from django.urls import reverse
from lessons.models import User

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.save()        
        
    def test_student_lessons_not_logged_in(self):
        response = self.client.get(reverse('student_lessons'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
                
    def test_student_lessons_when_logged_in(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('student_lessons'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_lessons.html')