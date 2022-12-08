# from django.test import TestCase, Client
# from django.urls import reverse
# from lessons.forms import LessonForm
# from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment
# 
# class TestViews(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.email = 'dummy@example.com'
#         self.password = 'Password123'
#         user = User.objects.create(email=self.email)
#         user.set_password(self.password)
#         user.save()
# 
#     def test_student_booking_not_logged_in(self):
#         response = self.client.get(reverse('student_booking'))
#         self.assertEquals(response.status_code, 200)
        
    #def test_student_booking(self):
    #    self.client.login(email=self.email, password=self.password)
    #    response = self.client.post(reverse('student_booking'))
    #    self.assertTemplateUsed(response, 'student_booking.html')