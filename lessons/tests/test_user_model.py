from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import User

class UserModelTestCase(TestCase):
    '''Unit test for the User model'''

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = 'John',
            last_name = 'Doe',
            email = 'james@example.org',
            password = 'Password123',
        )

    def test_valid_user(self):
        self.assert_user_is_valid()

    def test_email_cannot_be_blank(self):
        self.user.email = ''
        self.assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = self.create_second_user()
        self.user.email = second_user.email
        self.assert_user_is_invalid()

    def test_email_may_contain_numbers(self):
        self.user.email = 'james123@example.org'
        self.assert_user_is_valid()

    def test_email_must_contain_only_one_at(self):
        self.user.email = 'james@@example.org'
        self.assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@.org'
        self.assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@example'
        self.assert_user_is_invalid()

    def test_first_name_must_must_not_be_blank(self):
        self.user.first_name = ''
        self.assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = self.create_second_user()
        self.user.first_name = second_user.first_name
        self.assert_user_is_valid()

    def test_first_name_must_may_contain_50_characters(self):
            self.user.first_name = 'x'*50
            self.assert_user_is_valid()

    def test_first_name_must_cannot_contain_more_than_50_characters(self):
            self.user.first_name = 'x'*51
            self.assert_user_is_invalid()

    def test_last_name_must_must_not_be_blank(self):
        self.user.last_name = ''
        self.assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = self.create_second_user()
        self.user.last_name = second_user.last_name
        self.assert_user_is_valid()

    def test_last_name_must_may_contain_50_characters(self):
            self.user.last_name = 'x'*50
            self.assert_user_is_valid()

    def test_last_name_must_cannot_contain_more_than_50_characters(self):
            self.user.last_name = 'x'*51
            self.assert_user_is_invalid()

    def test_create_valid_superuser(self):
        director = User.objects.create_superuser(
            first_name = 'John',
            last_name = 'Doe',
            email = 'admin@example.org',
            password = 'Password123',
            is_staff = True,
            is_superuser = True
        )
        self.user = director
        self.assert_user_is_valid()

    def test_create_superuser_not_staff(self):
        with self.assertRaises(ValueError):
            director = User.objects.create_superuser(
                first_name = 'John',
                last_name = 'Doe',
                email = 'admin@example.org',
                password = 'Password123',
                is_staff = False,
                is_superuser = True
            )

    def test_create_superuser_not_superuser(self):
        with self.assertRaises(ValueError):
            director = User.objects.create_superuser(
                first_name = 'John',
                last_name = 'Doe',
                email = 'admin@example.org',
                password = 'Password123',
                is_staff = True,
                is_superuser = False
            )

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            self.user = User.objects.create_user(
                first_name = 'John',
                last_name = 'Doe',
                email = None,
                password = 'Password123',
            )

    def assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except(ValidationError):
            self.fail('Test user should be valid')

    def assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def create_second_user(self):
        user = User.objects.create_user(
            first_name = 'Jane',
            last_name = 'Li',
            email = 'jane@example.org',
            password = 'Li123',
        )
        return user
