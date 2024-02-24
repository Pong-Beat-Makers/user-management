from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import models, serializers
import helper


class FriendshipView(APIView): # 받는 데이터: user_email, friend_email
    # 사용자의 친구목록 반환
    def get(self, request):
        user = helper.get_user(request, 'user_email')
        friendships = models.Friendship.objects.filter(user=user)
        friend_list = []
        for friendship in friendships:
            friend_list.append(friendship.friend)
        return Response(friend_list, status=status.HTTP_200_OK)

    # 친구 추가
    def post(self, request):
        serializer = serializers.FriendshipSerializer(data=request.data)

        if serializer.is_valid():
            user = helper.get_user(request, 'user_email')
            friend = helper.get_user(request, 'friend_email')

            serializer.create_friendship(user, friend)
            return Response({'success': 'Friend added'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 친구 삭제
    def delete(self, request):
        serializer = serializers.FriendshipSerializer(data=request.data)

        if serializer.is_valid():
            user = helper.get_user(request, 'user_email')
            friend = helper.get_user(request, 'friend_email')

            serializer.delete_friendship(user, friend)
            return Response({'success': 'Friend deleted'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request): # 친구 차단..? 엥
    #     serializer = serializers.FriendshipSerializer(data=request.data)

    #     user = helper.get_user(request, 'user_email')
    #     friend = helper.get_user(request, 'friend_email')
    #     if serializer.is_valid():

