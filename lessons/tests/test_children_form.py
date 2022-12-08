from django.test import TestCase
from lessons.models import User, Children
from lessons.forms import ChildrenForm

class ChildrenFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'john.doe@example.org',
            first_name='John',
            last_name = 'Doe',
            password = 'Password123',
        )
        self.form_input = {
            'first_name':'Alice',
            'last_name': 'Doe',
            'age': '5',
            'email': 'alice.doe@example.org'
        }

    def test_valid_children_form(self):
        form = ChildrenForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_children_form_has_necessary_fields(self):
        form = ChildrenForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('age', form.fields)
        self.assertIn('email', form.fields)

    def test_children_negative_age(self):
        self.form_input['age']='-5'
        form = ChildrenForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_children_form_must_save_correctly(self):
        form = ChildrenForm(data = self.form_input)
        before_count = Children.objects.count()
        newChildren = form.save(commit=False)
        newChildren.parent = self.user
        newChildren.save()
        after_count = Children.objects.count()
        self.assertEqual(after_count, before_count+1)
        children = Children.objects.get(parent=self.user)
        self.assertEqual(children.first_name,'Alice')
        self.assertEqual(children.last_name,'Doe')
        self.assertEqual(children.age, 5)
        self.assertEqual(children.email,'alice.doe@example.org')

    def test_children_form_email_validation(self):
        self.form_input['email'] = 'bademail'
        form = ChildrenForm(data = self.form_input)
        self.assertFalse(form.is_valid())
