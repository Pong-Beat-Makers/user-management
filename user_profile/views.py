from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import serializers
from friends.models import Friendship
from social_login.models import User
import helper


class UserProfileView(APIView): # request에 있어야 하는 정보: 현재 사용자의 email(user_email), 찾고자 하는 사용자의 email(friend_email)
    # 특정유저 조회
    def get(self, request):
        user = helper.get_user(request, 'user_email')
        friend = helper.get_user(request, 'friend_email')
        is_friend = Friendship.objects.filter(user=user, friend=friend).exists()
        return Response({
            'nickname': friend.nickname,
            'profile': friend.profile,
            'status_message': friend.status_message,
            'win': friend.win,
            'lose': friend.lose,
            'rank': friend.rank,
            'is_friend': is_friend # 자기 자신을 조회할 경우 프론트에서 사용되지 않으므로 False여도 상관 없음
        }, status=status.HTTP_200_OK)

    # 유저 프로필 수정
    def put(self, request):
        serializer = serializers.ProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = helper.get_user(request, 'user_email')
            serializer.update(user, serializer.validated_data)  # 이미 있는 닉네임인 경우 ValidationError 발생, 400 status code 반환
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchUserView(APIView): # request에 있어야 하는 정보: 닉네임(keyword)
    # 닉네임으로 유저 검색
    def get(self, request):
        keyword = request.GET['keyword']
        matched_users = User.objects.filter(nickname__icontains=keyword)
        return Response([user.nickname for user in matched_users], status=status.HTTP_200_OK)
