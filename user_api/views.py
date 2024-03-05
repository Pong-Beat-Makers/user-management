from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class VerifyUserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'nickname': request.user.nickname},status=status.HTTP_200_OK)
        return Response({'error': 'Not Authenticated'}, status=status.HTTP_401_UNAUTHORIZED)