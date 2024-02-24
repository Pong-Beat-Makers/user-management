from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.UserProfileView.as_view(), name='user_profile'),
    path('edit/', views.UserProfileView.as_view(), name='user_profile_edit')
]
