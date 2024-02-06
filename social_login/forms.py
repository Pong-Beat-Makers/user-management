from django import forms
from allauth.account.forms import SignupForm
from .models import User


class SocialLoginSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(SocialLoginSignupForm, self).__init__(*args, **kwargs)
        nickname = forms.CharField(max_length=15, label='nickname')

    def custom_signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']

        user.save()


# class SocialLoginSignupForm(SignupForm):
#     nickname = forms.CharField(max_length=15, label='Nickname')  # 클래스 속성으로 정의합니다.
#
#     def custom_signup(self, request, user):
#         # 사용자의 닉네임을 사용자 모델에 저장합니다.
#         user.nickname = self.cleaned_data['nickname']
#         user.save()
#
#     def save(self, request):
#         # 사용자 객체를 만들고, 사용자 정보를 저장합니다.
#         user = super(SocialLoginSignupForm, self).save(request)
#         self.custom_signup(request, user)
#         return user
