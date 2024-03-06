from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status

class IsAuthenticatedAndActive(BasePermission):
	def has_permission(self, request, view):
		return request.user and request.user.is_authenticated and request.user.is_active

class UserPermissionMixin:
    permission_classes = [IsAuthenticatedAndActive]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not request.user.is_active:
            return Response({'error': 'not active'}, status=status.HTTP_403_FORBIDDEN)
        return super().dispatch(request, *args, **kwargs)
