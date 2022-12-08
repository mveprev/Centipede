from django.test import TestCase, Client
from django.urls import reverse
from lessons.forms import LessonForm
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment
from datetime import date

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

        term = TermDates.objects.create(
            name="Term 1",
            start_date=date(2022, 12, 1),
            end_date=date(2022, 12, 12)
        )
        term.save()

        lesson = Lesson.objects.create(term=term, lessons = 1, desiredInterval = 1, duration = 1, id = 1, user_id = 1, children = None)
        lesson.save()

        self.form_input = {
            'term': 1,
            'lesson': 1,
            'mondayMorning':True,
            'lessons':1,
            'desiredInterval':7,
            'duration':30,
            'furtherInfo':'I want to learn piano'
        }

    def test_get_lesson_view(self):
        response = self.client.get(reverse('student_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LessonForm))
        self.assertFalse(form.is_bound)

    def test_successful_lesson_form(self):
        before_count = Lesson.objects.count()
        response = self.client.post(reverse('student_booking'), self.form_input, follow=True)
        after_count = Lesson.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('student_booking')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_edit_lesson(self):
        response = self.client.get(reverse('edit-lesson', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_lessons.html')

    def test_successful_edit_lesson_form(self):
        before_count = Lesson.objects.count()
        response = self.client.post(reverse('edit-lesson', args=[1]), self.form_input, follow=True)
        after_count = Lesson.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('student_lessons')

    # def test_edit_lesson_POST(self):
    #     response = self.client.post(reverse('edit-lesson', args=[1]), {
    #     'term':TermDates.objects.create(name = 'test2', start_date='2023-01-01', end_date='2023-12-31'),
    #     'lessons':1, 'desiredInterval':1,
    #     'duration':1, 'id':1, 'user_id':1})
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'student_lessons.html')
