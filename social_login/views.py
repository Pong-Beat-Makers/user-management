from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from . import models
import requests, os
# access토큰 payload에 nickname추가
from .serializers import MyTokenObtainPairSerializer

LOGIN_URL, USER_INFO_URL, TOKEN_URL, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET, FE_URL, EV_URL = \
    None, None, None, None, None, None, None, None

def set_env(request):
    global LOGIN_URL, USER_INFO_URL, TOKEN_URL, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET, FE_URL, EV_URL
    path = request.path
    FE_URL = os.environ.get('FE_URL')
    EV_URL = os.environ.get('EV_URL')
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


def generate_new_nickname():
    last_record = models.User.objects.last()
    last_id = last_record.id if last_record else None
    return f'User{last_id + 1}' if last_id else 'User1'


class SocialLogin(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        set_env(request)
        return Response({
            'login_url': LOGIN_URL
        }, status=status.HTTP_200_OK)


class SocialLoginCallBack(APIView):
    permission_classes = [AllowAny]
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
        user = models.User.objects.filter(email=email).first()

        response = None
        if not user:
            user = models.User.objects.create_user(email=email, nickname=generate_new_nickname())
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f"http://127.0.0.1:8000/accounts/email_verification/{uid}/{token}/"

            subject = 'Email Verification'
            message = f'Please click this link to verify: {verification_url}'
            from_email = 'younghye0709@gmail.com'
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
            response = HttpResponseRedirect(EV_URL) # 이메일을 확인해주세요 화면 띄우기
        else:
            response = HttpResponseRedirect(FE_URL)

        refresh_token = MyTokenObtainPairSerializer.get_token(user)
        access_token = refresh_token.access_token
        response.set_cookie('access_token', str(access_token), httponly=True)
        return response

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

class EmailVerificationView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = models.User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, models.User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponseRedirect(FE_URL)
        else:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
