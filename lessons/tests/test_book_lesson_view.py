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

        student = User.objects.create_user(
            email = 'john.doe@example.org',
            first_name='John',
            last_name = 'Doe',
            password = 'Password123',
        )
        student.save()

        term = TermDates.objects.create(name = 'test', start_date=date(2022,1,1), end_date=date(2022,12,31))
        term.save()

        lesson = Lesson.objects.create(
            lessons=2,
            desiredInterval=7,
            duration=30,
            furtherInfo="I want to learn piano",
            user=student
        )
        lesson.save()
        valid_lesson_pk = Lesson.objects.all()[0].pk

        teacher = User.objects.create_user(
            email="dwayne.johnson@example.org",
            password="Password123",
            first_name="Dwayne",
            last_name="Johnson",
            is_teacher=True,
        )
        teacher.save()
        valid_teacher_pk = User.objects.filter(is_teacher=True)[0].pk

        self.form_input = {
            'teacher': str(valid_teacher_pk),
            'lesson': str(valid_lesson_pk),
            'start_time':time(22,12,00),
            'start_date':date(2023, 6, 1),
            'interval':7,
            'number_of_lessons':7,
            'duration': 45
        }


    def test_book_lesson(self):
        response = self.client.get(reverse('book-lesson', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_lessons.html')

    def test_book_lesson_post(self):
        response = self.client.post(reverse('book-lesson', args=[1]), self.form_input, follow=True)
        self.assertEquals(response.status_code, 200)
