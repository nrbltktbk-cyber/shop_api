from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('Пользователь успешно зарегистрирован'),
            400: 'Ошибка валидации'
        },
        operation_description="Регистрация нового пользователя с отправкой кода подтверждения на email"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Пользователь успешно зарегистрирован. Код подтверждения отправлен на email.',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'is_active': user.is_active
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=ConfirmSerializer,
        responses={
            200: openapi.Response('Email успешно подтвержден'),
            400: 'Ошибка валидации'
        },
        operation_description="Подтверждение email с помощью кода, полученного при регистрации"
    )
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validate(serializer.data)
            return Response({
                'message': 'Email успешно подтвержден. Теперь вы можете войти.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Успешный вход', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )),
            400: 'Ошибка валидации',
            401: 'Неверные учетные данные'
        },
        operation_description="Авторизация пользователя с получением токена"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Аутентифицируем пользователя
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            if user:
                if not user.is_active:
                    return Response(
                        {'error': 'Аккаунт не подтвержден. Подтвердите email.'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                # Создаем или получаем токен
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'phone_number': user.phone_number,
                        'is_active': user.is_active,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Неверный email или пароль'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)