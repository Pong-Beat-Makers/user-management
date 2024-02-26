from rest_framework import status
from rest_framework.response import Response
from social_login.models import User

# def get_user(user_email):
#     user = User.objects.filter(email=user_email).first()
#     if user is None:
#         raise AttributeError(f'user {user_email} not found')
#     return user
def get_user(user_pk):
    user = User.objects.filter(pk=user_pk).first()
    if user is None:
        raise AttributeError(f'user not found')
    return user
