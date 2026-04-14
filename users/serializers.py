from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import ConfirmationCode


# 🔐 Регистрация
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False  # ❗ неактивный
        )

        ConfirmationCode.objects.create(user=user)

        return user


# ✅ Подтверждение
class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            confirm = ConfirmationCode.objects.get(user=user)

            if confirm.code != data['code']:
                raise serializers.ValidationError("Неверный код")

            user.is_active = True
            user.save()
            confirm.delete()

        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        return data


# 🔑 Авторизация
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Неверные данные")

        if not user.is_active:
            raise serializers.ValidationError("Подтвердите аккаунт")

        return data