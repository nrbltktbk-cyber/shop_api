import os
import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.serializers import OAuthCodeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer

    def post(self, request):
        serialaizer = self.get_serializer(data=request.data)
        serialaizer.is_valid(raise_exception=True)
    
        code = serialaizer.validated_data['code']
    
        token_response = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': '475994727017-g0cjrdv719jd3ffcn73ib52lhl5p5u9m.apps.googleusercontent.com ',
        'client_secret': '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',
        'redirect_uri': 'http://localhost:8000/api/v1/user/google-login',
        'grant_type': 'authorization_code'
    })
    
        token_data = token_response.json()
        access_token = token_data.get('access_token')
    
        if not access_token:
            return Response({'error': 'Invalid access token'})
    
        user_info = requests.get(
            url='https://www.googleapis.com/oauth2/v1/userinfo',
            params={'alt': 'json'},
            headers={'Authorization': f"Bearer {access_token}"}
    ).json()
    
        print(f"USER INFO: {user_info}")
    
        email = user_info.get('email')
    
        user, created = User.objects.get_or_create(email=email)
    
        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
    
        return Response({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    })
