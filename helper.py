from rest_framework import status
from rest_framework.response import Response
from social_login.models import User

def get_user(request, email):
    user_email = request.GET[email]
    user = User.objects.filter(email=user_email).first()
    if user is None:
        return Response({'error': f'user {email} not found'}, status=status.HTTP_404_NOT_FOUND)
    return user
