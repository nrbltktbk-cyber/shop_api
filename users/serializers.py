from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import ConfirmationCode
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method

CustomUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Пароль пользователя"
    )
    email = serializers.EmailField(
        required=True,
        help_text="Email пользователя (используется как логин)"
    )
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Номер телефона (необязательно при регистрации)"
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone_number']
        swagger_schema_fields = {
            'description': 'Регистрация нового пользователя'
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            is_active=False
        )
        
        # Создаем код подтверждения
        ConfirmationCode.objects.create(user=user)
        
        return user


class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        help_text="Email пользователя"
    )
    code = serializers.CharField(
        max_length=6,
        required=True,
        help_text="6-значный код подтверждения"
    )
    
    class Meta:
        swagger_schema_fields = {
            'description': 'Подтверждение email с помощью кода'
        }
    
    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            confirm = ConfirmationCode.objects.get(user=user)
            
            if confirm.code != data['code']:
                raise serializers.ValidationError("Неверный код подтверждения")
            
            user.is_active = True
            user.save()
            confirm.delete()
            
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден")
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения не найден. Запросите новый код")
        
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, help_text="Email пользователя")
    password = serializers.CharField(required=True, style={'input_type': 'password'}, help_text="Пароль пользователя")
    
    class Meta:
        swagger_schema_fields = {
            'description': 'Авторизация пользователя'
        }
    
    def validate(self, data):
        # Не делаем здесь authenticate, только проверяем данные
        if not data.get('email') or not data.get('password'):
            raise serializers.ValidationError("Email и пароль обязательны")
        return data


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'is_active']