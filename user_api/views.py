from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from social_login.serializers import UserSerializer


class VerifyUserView(APIView):
    def get(self, request):
        try:
            serializers = UserSerializer(request.user)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
