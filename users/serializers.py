from rest_framework import serializers
from rest_framework.exceptions import ValidationError
#from .models import ConfirmationCode
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import utils

CustomUser = get_user_model()


class OAuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        return token


class UserBaseSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    def validate_username(self, email):
        try:
            CustomUser.objects.get(email=email)
        except:
            return email
        raise ValidationError("CustomUser уже существует!")
    
    


class ConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")
    
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError("Пользователь не найден!")

        if not utils.verify_confirmation_code(email, code):
            raise serializers.ValidationError("Неверный код подтверждения!")
    
        attrs["user"] = user
        return attrs
    
    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.is_active = True
        user.save()