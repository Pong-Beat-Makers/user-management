from django.urls import path
from . import views

# localhost:8000/profile/
urlpatterns = [
    path('', views.UserProfileView.as_view(), name='user_profile'),
    path('search/', views.SearchUserView.as_view(), name='user_search')
]
