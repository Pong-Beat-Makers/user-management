from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import serializers
from social_login.models import User
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import AllowAny


class FriendshipView(APIView):
    # 사용자의 친구목록 반환

    def get(self, request):
        try:
            user = request.user
            serializer = serializers.FriendshipSerializer(data=request.data)
            friend_list = serializer.get_friend_list(user)
            return Response(friend_list, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    # 친구 추가
    def post(self, request):  # 받는 데이터(Body): id
        try:
            user = request.user
            friend = User.objects.get(id=request.data['id'])
            serializer = serializers.FriendshipSerializer(data=request.data)
            if serializer.is_valid():
                friendship = serializer.create_friendship(user, friend)
                return Response(
                    {'success': f'{friendship.user.nickname} added {friendship.friend.nickname} as a friend'},
                    status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': f"friend {request.data['friend']} not found"}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    # 친구 삭제
    def delete(self, request):  # 받는 데이터(Body): id
        try:
            user = request.user
            friend = User.objects.get(id=request.data['id'])
            serializer = serializers.FriendshipSerializer(data=request.data)
            serializer.delete_friendship(user, friend)
            return Response({'success': f'{user.nickname} deleted friend {friend.nickname}'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': f"friend {request.data['friend']} not found"}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class s2s_FriendshipView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            user_id = request.GET['id']
            user = User.objects.get(id=user_id)
            serializer = serializers.FriendshipSerializer()
            friend_list = serializer.get_friend_list(user)
            return Response(friend_list, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': "user not found"}, status=status.HTTP_404_NOT_FOUND)
