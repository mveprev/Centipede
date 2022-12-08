from django.test import TestCase, Client
from django.urls import reverse
from lessons.forms import LessonForm, DateForm
from lessons.models import User, Lesson, Children, TermDates, Schedule, Payment
from datetime import date

#Test for my_children in views.py
class TestViews(TestCase):
    def setUp(self):
        self.url = reverse('term_dates')
        self.form_input = {
            'name':'Term 0',
            'start_date': date(2003, 4, 1),
            'end_date': date(2003, 4, 14),
        }
        self.client = Client()
        self.email = 'dummy@example.com'
        self.password = 'Password123'
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.is_staff=True
        user.save()
        self.client.login(email=self.email, password=self.password)

        term = TermDates.objects.create(name = 'test', start_date='2022-01-01', end_date='2022-12-31')
        term.save()

        lesson = Lesson.objects.create(term=TermDates.objects.first(), lessons = 1, desiredInterval = 1, duration = 1, id = 1, user_id = 1, children = None)
        lesson.save()

    def test_get_test_dates(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_dates.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, DateForm))
        self.assertTrue(form.is_bound)

    def test_successful_term_dates(self):
        before_count = TermDates.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = TermDates.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('view_term_dates')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        user = TermDates.objects.get(name = 'Term 0')
        self.assertEqual(user.start_date,date(2003, 4, 1))
        self.assertEqual(user.end_date,date(2003, 4, 14))

    def test_view_term_dates_get(self):
        response = self.client.get(reverse('edit_term_dates', args=[1]))
        self.assertEquals(response.status_code, 200)

    def test_view_term_dates_post(self):
        response = self.client.post(reverse('edit_term_dates', args=[1]),{
        'start_date':'2022-01-01',
        'end_date':'2022-12-31'
        })
        self.assertEquals(response.status_code, 200)

    def test_successful_edit_term_dates(self):
        before_count = TermDates.objects.count()
        response = self.client.post(reverse('edit_term_dates', args=[1]), self.form_input, follow=True)
        after_count = TermDates.objects.count()
        self.assertEqual(after_count, before_count)
