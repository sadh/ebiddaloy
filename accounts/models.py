from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class SchoolUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)


class Teacher(models.Model):
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)


class Admin(models.Model):
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)


class Parent(models.Model):
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)