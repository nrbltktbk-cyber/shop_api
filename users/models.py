from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
import random

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # необязательный
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # phone_number не обязателен для регистрации
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Делаем phone_number обязательным только для суперпользователя
        if self.is_superuser and not self.phone_number:
            raise ValueError("Суперпользователь должен указать номер телефона")
        super().save(*args, **kwargs)


class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.email}: {self.code}'