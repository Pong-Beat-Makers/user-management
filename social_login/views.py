from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str # force_text는 오류 떠서 일단 지움.
from .models import User
from . import utils
# access토큰 payload에 nickname추가
from .serializers import MyTokenObtainPairSerializer


class SocialLogin(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        utils.set_env(request)
        print(utils.LOGIN_URL)
        return Response({
            'login_url': utils.LOGIN_URL
        }, status=status.HTTP_200_OK)


class SocialLoginCallBack(APIView):
    permission_classes = [AllowAny]
    def get(self, request):

        if request.user.is_authenticated:
            return Response({'error': 'already logged in'}, status=status.HTTP_200_OK)
        code = request.GET['code']

        if not code:
            return Response({'error': 'code is required'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = utils.get_access_token(code)
        if not access_token:
            return Response({'error': 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = utils.get_user_info(access_token)
        email = user_info.get('email')
        user = User.objects.filter(email=email).first()

        response = None
        if not user or not user.is_active:
            if not user:
                user = User.objects.create_user(email=email, nickname=utils.generate_new_nickname())
            utils.send_verification_email(user, request)
            # response = HttpResponseRedirect(utils.EV_URL) # 이메일을 확인해주세요 화면 띄우기
            response = Response({'error': 'Please verify your email'}, status=status.HTTP_400_BAD_REQUEST) # 임시 화면
        else:
            response = HttpResponseRedirect(utils.FE_URL)

        refresh_token = MyTokenObtainPairSerializer.get_token(user)
        access_token = refresh_token.access_token
        response.set_cookie('access_token', str(access_token), httponly=True)

        return response


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponseRedirect(utils.FE_URL)
        else:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
