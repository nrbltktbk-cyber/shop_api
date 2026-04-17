from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer


# 🔐 Регистрация
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Пользователь создан. Подтвердите код."
        }, status=status.HTTP_201_CREATED)


# ✅ Подтверждение
class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "message": "Аккаунт подтвержден"
        })


# 🔑 Авторизация
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "message": "Успешный вход"
        })