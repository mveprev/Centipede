"""Models in the Lessons app."""

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, User
from msms import settings



class UserManager(BaseUserManager):
    """Manage user model objects"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('outstanding_balance', 0)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model used for authentication"""

    email = models.EmailField(
        unique=True,
        max_length=50,
        blank=False,
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_teacher = models.BooleanField(default=False, verbose_name='teacher')
    is_staff = models.BooleanField(default=False, verbose_name='administrator')
    is_superuser = models.BooleanField(default=False, verbose_name='director')
    is_active = models.BooleanField(default=True, verbose_name='active')
    outstanding_balance = models.IntegerField(default=0, blank=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

class Children(models.Model):
    """Children model used for child details"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(blank=False)
    email = models.CharField(max_length=50, blank=True, null=True)
    id = models.AutoField(primary_key=True, unique=True)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)


class TermDates(models.Model):
    """Model used for term dates """

    name = models.CharField(max_length = 50, default = 'default', unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

class Lesson(models.Model):
    """Lesson model used for booking lessons"""

    term = models.ForeignKey(TermDates, on_delete=models.CASCADE, null=True)

    mondayMorning = models.BooleanField(default=False)
    mondayAfternoon = models.BooleanField(default=False)
    mondayNight = models.BooleanField(default=False)
    tuesdayMorning = models.BooleanField(default=False)
    tuesdayAfternoon = models.BooleanField(default=False)
    tuesdayNight = models.BooleanField(default=False)
    wednesdayMorning = models.BooleanField(default=False)
    wednesdayAfternoon = models.BooleanField(default=False)
    wednesdayNight = models.BooleanField(default=False)
    thursdayMorning = models.BooleanField(default=False)
    thursdayAfternoon = models.BooleanField(default=False)
    thursdayNight = models.BooleanField(default=False)
    fridayMorning = models.BooleanField(default=False)
    fridayAfternoon = models.BooleanField(default=False)
    fridayNight = models.BooleanField(default=False)

    lessons = models.IntegerField(blank=False)
    desiredInterval = models.IntegerField(blank=False)
    duration = models.IntegerField(blank=False)
    furtherInfo = models.TextField()
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    children = models.ForeignKey(Children, on_delete=models.CASCADE, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    invoiceNum = models.CharField(max_length = 50, default = 'default')
    studentNum = models.CharField(max_length = 50, default = 'default')
    invoiceEmail = models.CharField(max_length = 50, default = 'default')

class Schedule(models.Model):
    """Model for schedule details"""

    time_stamp = models.DateTimeField(auto_now = True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now = False)
    start_date = models.DateField(blank=False)
    interval = models.IntegerField(blank=False)
    number_of_lessons = models.IntegerField(blank=False)
    duration = models.IntegerField(blank=False)


class Payment(models.Model):
    """Model for payment details"""

    payment_time = models.DateTimeField(auto_now = True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_paid = models.IntegerField(blank=False)
    balance_before = models.IntegerField(default=0, blank=False)
    balance_after = models.IntegerField(default=0, blank=False)
