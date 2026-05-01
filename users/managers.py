from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Устанавливаем обязательные поля
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Проверяем, что phone_number указан для суперпользователя
        if 'phone_number' not in extra_fields or not extra_fields['phone_number']:
            raise ValueError('Суперпользователь должен указать phone_number')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True for superuser')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True for superuser')
        if extra_fields.get('is_active') is not True:
            raise ValueError('is_active must be True for superuser')
        
        return self.create_user(email, password, **extra_fields)