from django.contrib import admin
from django.urls import path, include
from .views import SocialLogin, SocialLoginCallBack
from . import views

urlpatterns = [
	path('google/login/', SocialLogin.as_view(), name='google_login'),
	path('42intra/login/', SocialLogin.as_view(), name='42intra_login'),
	path('google/login/callback/', SocialLoginCallBack.as_view(), name='google_callback'),
	path('42intra/login/callback/', SocialLoginCallBack.as_view(), name='intra_callback')
]
