from django.urls import path
from . import views

# localhost:8000/friends/
urlpatterns = [
    path('', views.FriendshipView.as_view(), name='friend'),
    path('friendlist/', views.s2s_FriendshipView.as_view(), name='s2s_friendship'),
    path('friendaddme/', views.s2s_FriendAddMeview.as_view(), name='s2s_user_as_friend'),
]
