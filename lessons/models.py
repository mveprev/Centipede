from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from msms import settings
# Create your models here.

class StudentManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        student = self.model(email=email, **extra_fields)
        student.set_password(password)
        student.save(using=self._db)
        return student

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

class Student(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        unique = True,
        max_length = 50,
        blank = False,
    )
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank = False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = StudentManager()
    USERNAME_FIELD = 'email'
