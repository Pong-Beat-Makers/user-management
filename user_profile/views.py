from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import serializers
from friends.models import Friendship
from social_login.models import User
import userManagement.helper as helper


class UserProfileView(APIView):
    # 특정유저 조회
    def get(self, request): # 받는 데이터(Query): user, friend
        user_pk = request.GET['user']
        friend_pk = request.GET['friend']
        try:
            user = helper.get_user(user_pk)
            friend = helper.get_user(friend_pk)
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
        except AttributeError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # 수정할것: 자기 자신만 수정 가능하도록 수정
    # 유저 프로필 수정
    def patch(self, request): # 받는 데이터(Body): user, profile_to, nickname_to, status_message_to
        user_pk = request.data['user']
        try:
            user = helper.get_user(user_pk)

            serializer = serializers.ProfileSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.update(user, serializer.validated_data): # 이미 있는 닉네임인 경우 ValidationError 발생, 400 status code 반환
                    return Response({'message': 'success'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

class SearchUserView(APIView): # 받는 데이터(Query): keyword
    # 수정할것: 자기 자신은 제외하고 닉네임으로 유저 검색
    # 닉네임으로 유저 검색
    def get(self, request):
        keyword = request.GET['keyword']
        matched_users = User.objects.filter(nickname__icontains=keyword)
        return Response([user.nickname for user in matched_users], status=status.HTTP_200_OK)
