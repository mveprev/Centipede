from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, User
from django.core.validators import MaxValueValidator, MinValueValidator 
from msms import settings
# Create your models here.


class UserManager(BaseUserManager):

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

    email = models.EmailField(
        unique=True,
        max_length=50,
        blank=False,
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_staff = models.BooleanField(default=False, verbose_name='administrator')
    is_superuser = models.BooleanField(default=False, verbose_name='director')
    is_active = models.BooleanField(default=True, verbose_name='active')

    objects = UserManager()
    USERNAME_FIELD = 'email'

class Children(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(blank=False)
    email = models.CharField(max_length=50, blank=True, null=True)
    id = models.AutoField(primary_key=True, unique=True)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)

class Lesson(models.Model):
    availabilityDay = models.CharField(max_length=100, blank=False)
    availabilityTime = models.CharField(max_length=100, blank=False)
    lessons = models.IntegerField(validators=[MaxValueValidator(4)],blank=False)
    desiredInterval = models.CharField(max_length=100, blank=False)
    duration = models.IntegerField(blank=False)
    furtherInfo = models.TextField()
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    children = models.ForeignKey(Children, on_delete=models.CASCADE, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    invoiceNum = models.CharField(max_length = 50, default = 'default')
    studentNum = models.CharField(max_length = 50, default = 'default')
    invoiceEmail = models.CharField(max_length = 50, default = 'default')

class TermDates(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
