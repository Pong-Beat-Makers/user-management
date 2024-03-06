from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import serializers
from social_login.models import User
from userManagement.permissions import UserPermissionMixin


class UserProfileView(UserPermissionMixin, APIView):
    # 특정유저 조회
    def get(self, request):  # 받는 데이터(Query): user, friend
        user_pk = request.GET['user']
        friend_pk = request.GET['friend']
        try:
            # user = request.user
            user = User.objects.get(pk=user_pk)
            friend = User.objects.get(pk=friend_pk)
            serializer = serializers.ProfileSerializer(data=request.data)
            info = serializer.get_user_info(user, friend)
            return Response(info, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': f'friend {friend_pk} not found'}, status=status.HTTP_404_NOT_FOUND)

    # 유저 프로필 수정
    def patch(self, request):  # 받는 데이터(Body): user, profile_to, nickname_to, status_message_to
        user_pk = request.data['user']
        try:
            # user = request.user
            user = User.objects.get(pk=user_pk)
            # if user != User.objects.get(pk=user_pk)
            # return Response({'error': 'You cannot modify other user\'s profile'}, status=status.HTTP_403_FORBIDDEN)
            serializer = serializers.ProfileSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.update(user,
                                     serializer.validated_data):  # 이미 있는 닉네임인 경우 ValidationError 발생, 400 status code 반환
                    return Response({'message': 'success'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': f'user {user_pk} not found'}, status=status.HTTP_404_NOT_FOUND)


class SearchUserView(UserPermissionMixin, APIView):  # 받는 데이터(Query): keyword
    # 닉네임으로 유저 검색
    def get(self, request):
        keyword = request.GET['keyword']
        # matched_users = User.objects.filter(nickname__icontains=keyword).exclude(nickname=request.user.nickname)
        matched_users = User.objects.filter(nickname__icontains=keyword)
        return Response([user.nickname for user in matched_users], status=status.HTTP_200_OK)
