from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)

    first_name = models.CharField(
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        max_length=150,
        blank=True
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    REGISTRATION_SOURCE_CHOICES = [
        ('local', 'Local registration'),
        ('google', 'Google OAuth'),
        ('facebook', 'Facebook OAuth'),
    ]

    registration_source = models.CharField(
        max_length=20,
        choices=REGISTRATION_SOURCE_CHOICES,
        default='local'
    )

    google_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    last_login_google = models.DateTimeField(
        blank=True,
        null=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class ConfirmationCode(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="confirmation_code"
    )

    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(
        auto_now_add=True
    )