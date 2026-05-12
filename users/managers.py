from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email,
            password,
            **extra_fields
        )

    def get_or_create_google_user(
        self,
        email,
        google_id,
        first_name="",
        last_name=""
    ):

        user, created = self.get_or_create(
            email=email,
            defaults={
                "google_id": google_id,
                "first_name": first_name,
                "last_name": last_name,
                "registration_source": "google",
                "is_active": True,
            }
        )

        user.last_login = timezone.now()
        user.last_login_google = timezone.now()

        user.save()

        return user, created