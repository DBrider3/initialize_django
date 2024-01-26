# System
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

# Project
from core.models import BaseModel
from app.users.managers import MyUserManager


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        app_label = "users"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser
