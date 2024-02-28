from django.urls import path
from . import views

# localhost:8000/friends/
urlpatterns = [
    path('', views.FriendshipView.as_view(), name='friend'),
    path('<int:user_pk>/delete/<int:friend_pk>', views.FriendshipView.as_view(), name='delete_friend'),
]
