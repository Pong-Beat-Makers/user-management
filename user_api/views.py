from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from social_login.serializers import UserSerializer

# Create your views here.
class VerifyUserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializers = UserSerializer(request.user)
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response({'error': 'Not Authenticated'}, status=status.HTTP_401_UNAUTHORIZED)