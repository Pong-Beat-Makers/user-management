from django.contrib import admin
from django.urls import path, include
from .views import SocialLogin, SocialLoginCallBack
from . import views

urlpatterns = [
	path('accounts/google/login/', SocialLogin.as_view(), name='google_login'),
	path('accounts/42intra/login/', SocialLogin.as_view(), name='42intra_login'),
	path('accounts/google/login/callback/', SocialLoginCallBack.as_view(), name='google_callback'),
	path('accounts/42intra/login/callback/', SocialLoginCallBack.as_view(), name='intra_callback')
]
