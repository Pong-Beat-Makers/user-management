from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.FriendshipView.as_view(), name='add_friend'),
    path('delete/', views.FriendshipView.as_view(), name='delete_friend'),
]
