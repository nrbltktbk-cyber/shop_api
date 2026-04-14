from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer


# 🔐 Регистрация
@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({
        "message": "Пользователь создан. Подтвердите код."
    }, status=status.HTTP_201_CREATED)


# ✅ Подтверждение
@api_view(['POST'])
def confirm_view(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    return Response({
        "message": "Аккаунт подтвержден"
    })


# 🔑 Авторизация
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    return Response({
        "message": "Успешный вход"
    })