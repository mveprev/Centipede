from django.test import TestCase, Client
from django.urls import reverse
from lessons.forms import LessonForm
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment
from datetime import time, date

#Test for book_lesson in views.py
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        self.admin = True
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.is_staff = True
        user.save()
        self.client.login(email=self.email, password=self.password)

        self.student=User.objects.create(email='john@kcl.ac.uk')
        self.student.set_password(self.password)
        self.student.save()

        term = TermDates.objects.create(name = 'test', start_date=date(2022,1,1), end_date=date(2022,12,31))
        term.save()

        lesson = Lesson.objects.create(term=TermDates.objects.first(), lessons = 1, desiredInterval = 7, duration = 30, furtherInfo="I want to learn piano", id = 1, user = self.student, children = None)
        lesson.save()

        self.teacher = User.objects.create(email='teacher@test.com')
        self.teacher.is_teacher = True
        self.teacher.first_name = 'test'
        self.teacher.last_name = 'test'
        self.teacher.outstanding_balance = 0
        self.teacher.save()


    def test_book_lesson(self):
        response = self.client.get(reverse('book-lesson', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_lessons.html')

    def test_book_lesson_get(self):
        response = self.client.post(reverse('book-lesson', args=[1]), {
            'teacher': self.teacher,
            'start_time':time(10,12,00),
            'start_date':date(2022, 6, 1),
            'interval':7,
            'number_of_lessons':2,
            'duration': 30
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_lessons.html')
