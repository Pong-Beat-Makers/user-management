from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import models, serializers
import userManagement.helper as helper


class FriendshipView(APIView):
    # 사용자의 친구목록 반환
    def get(self, request): # 받는 데이터(Query): user
        user_pk = request.GET['user']
        try:
            user = helper.get_user(user_pk)
            friendships = models.Friendship.objects.filter(user=user)
            friend_list = []
            for friendship in friendships:
                friend_data = {
                    'pk': friendship.friend.pk,
                    'email': friendship.friend.email,
                    'nickname': friendship.friend.nickname,
                    'profile': friendship.friend.profile
                }
                friend_list.append(friend_data)
            return Response(friend_list, status=status.HTTP_200_OK)
        except AttributeError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # 친구 추가
    def post(self, request): # 받는 데이터(Body): user, friend
        user_pk = request.data['user']
        friend_pk = request.data['friend']

        try:
            user = helper.get_user(user_pk)
            friend = helper.get_user(friend_pk)
            serializer = serializers.FriendshipSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create_friendship(user, friend)
                return Response({'success': 'Friend added'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # 친구 삭제
    def delete(self, request): # 받는 데이터(Query): user, friend
        user_pk = request.GET['user']
        friend_pk = request.GET['friend']

        try:
            user = helper.get_user(user_pk)
            friend = helper.get_user(friend_pk)

            if user == friend:
                raise Exception('You cannot delete yourself as a friend')
            friendship = models.Friendship.objects.filter(user=user, friend=friend).first()
            if friendship is None:
                raise Exception('You are not friends')
            friendship.delete()
            return Response({'success': 'Friend deleted'}, status=status.HTTP_200_OK)
        except AttributeError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request): # 친구 차단..? 엥
    #     serializer = serializers.FriendshipSerializer(data=request.data)

    #     user = helper.get_user(request, 'user_email')
    #     friend = helper.get_user(request, 'friend_email')
    #     if serializer.is_valid():

