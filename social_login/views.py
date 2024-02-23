from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from .models import User
import os

# 랜덤 스트링
import random
import string

LOGIN_URL, USER_INFO_URL, TOKEN_URL, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET = None, None, None, None, None, None


def set_env(request):
    global LOGIN_URL, USER_INFO_URL, TOKEN_URL, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
    path = request.path
    if 'google' in path:
        LOGIN_URL = (
                'https://accounts.google.com/o/oauth2/v2/auth' +
                '?client_id=' + os.environ.get('GOOGLE_CLIENT_ID') +
                '&redirect_uri=' + os.environ.get('GOOGLE_URI') +
                '&response_type=code' +
                '&scope=email%20profile'
        )
        USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/tokeninfo'
        TOKEN_URL = 'https://oauth2.googleapis.com/token'
        REDIRECT_URI = os.environ.get('GOOGLE_URI')
        CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
        CLIENT_SECRET = os.environ.get('GOOGLE_SECRET')
    elif '42intra' in path:
        LOGIN_URL = (
                os.environ.get('INTRA_API_URL') + '/oauth/authorize' +
                '?client_id=' + os.environ.get('INTRA_CLIENT_ID') +
                '&redirect_uri=' + os.environ.get('INTRA_URI') +
                '&response_type=code'
        )
        USER_INFO_URL = os.environ.get('INTRA_API_URL') + '/v2/me'
        TOKEN_URL = os.environ.get('INTRA_API_URL') + '/oauth/token'
        REDIRECT_URI = os.environ.get('INTRA_URI')
        CLIENT_ID = os.environ.get('INTRA_CLIENT_ID')
        CLIENT_SECRET = os.environ.get('INTRA_SECRET')


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


# Create your views here.

class SocialLogin(APIView):
    def get(self, request):
        set_env(request)
        return Response({
            'login_url': LOGIN_URL
        }, status=status.HTTP_200_OK)

class SocialLoginCallBack(APIView):
    def get(self, request):

        if request.user.is_authenticated:
            return Response({'error': 'already logged in'}, status=status.HTTP_200_OK)
        code = request.GET['code']

        if not code:
            return Response({'error': 'code is required'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = self.get_access_token(code)
        if not access_token:
            return Response({'error': 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = self.get_user_info(access_token)
        email = user_info.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            user = User.objects.create_user(email=email, nickname=generate_random_string(10))

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        redirect('http://127.0.0.1:5501').set_cookie('refresh_token', refresh_token).set_cookie('access_token', access_token)
    def get_user_info(self, access_token):
        response = requests.get(USER_INFO_URL + f'?access_token={access_token}')
        if response.status_code == 200:
            user_info = response.json()
            return user_info

    def get_access_token(self, code):
        data = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI,
        }
        response = requests.post(TOKEN_URL, data=data)
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
