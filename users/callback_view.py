# views.py

import requests

from django.conf import settings
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class GoogleCallbackView(APIView):

    def get(self, request):

        code = request.GET.get("code")

        return Response({
            "code": code
        })