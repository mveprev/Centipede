from django.test import TestCase, Client
from django.urls import reverse
from lessons.forms import LessonForm
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment

#Test for edit_lesson in views.py
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.save()
        self.client.login(email=self.email, password=self.password)
        
        term = TermDates.objects.create(name = 'test', start_date='2022-01-01', end_date='2022-12-31')
        term.save()
        
        lesson = Lesson.objects.create(term=TermDates.objects.first(), lessons = 1, desiredInterval = 1, duration = 1, id = 1, user_id = 1, children = None)
        lesson.save()
        
    def test_edit_lesson(self):
        response = self.client.get(reverse('edit-lesson', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_lessons.html')
        
    # def test_edit_lesson_POST(self):
    #     response = self.client.post(reverse('edit-lesson', args=[1]), {
    #     'term':TermDates.objects.create(name = 'test2', start_date='2023-01-01', end_date='2023-12-31'), 
    #     'lessons':1, 'desiredInterval':1, 
    #     'duration':1, 'id':1, 'user_id':1})
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'student_lessons.html')


    