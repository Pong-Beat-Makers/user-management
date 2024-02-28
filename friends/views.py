from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import serializers
from social_login.models import User
from rest_framework.permissions import IsAuthenticated


class FriendshipView(APIView):
    # 사용자의 친구목록 반환
    def get(self, request):  # 받는 데이터(Query): user -> IsAuthenticated 사용하면 request.user로 받을 수 있음
        user_pk = request.GET['user']
        # permission_classes = [IsAuthenticated]
        try:
            # user = request.user
            user = User.objects.get(pk=user_pk)
            serializer = serializers.FriendshipSerializer(data=request.data)
            friend_list = serializer.get_friend_list(user)
            return Response(friend_list, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': f'user {user_pk} not found'}, status=status.HTTP_404_NOT_FOUND)

    # 친구 추가
    def post(self, request):  # 받는 데이터(Body): user, friend
        # permission_classes = [IsAuthenticated]
        try:
            serializer = serializers.FriendshipSerializer(data=request.data)
            if serializer.is_valid():
                user_pk = serializer.validated_data['user']['pk']  # user_pk = request.data['user']?
                friend_pk = serializer.validated_data['friend']['pk']
                # user = request.user
                user = User.objects.get(pk=user_pk)
                friend = User.objects.get(pk=friend_pk)
                friendship = serializer.create_friendship(user, friend)
                return Response(
                    {'success': f'{friendship.user.nickname} added {friendship.friend.nickname} as a friend'},
                    status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # 친구 삭제
    def delete(self, request, user_pk, friend_pk):  # 받는 데이터(URL parameter): user, friend
        # permission_classes = [IsAuthenticated]
        try:
            # user = request.user
            user = User.objects.get(pk=user_pk)
            friend = User.objects.get(pk=friend_pk)
            serializer = serializers.FriendshipSerializer(data=request.data)
            serializer.delete_friendship(user, friend)
            return Response({'success': f'{user.nickname} deleted friend {friend.nickname}'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': f'friend {friend_pk} not found'}, status=status.HTTP_404_NOT_FOUND)

    # def put(self, request): # 친구 차단..? 엥
    #     serializer = serializers.FriendshipSerializer(data=request.data)

    #     user = helper.get_user(request, 'user_email')
    #     friend = helper.get_user(request, 'friend_email')
    #     if serializer.is_valid():
