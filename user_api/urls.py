from django.urls import path
from .views import VerifyUserView

urlpatterns = [
    path('verify/', VerifyUserView.as_view(), name='user_verify')
]