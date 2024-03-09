from rest_framework import serializers
from .models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    friend = serializers.CharField()

    class Meta:
        model = Friendship
        fields = ['friend']

    def get_friend_list(self, user):
        friendships = Friendship.objects.filter(user=user)
        friend_list = []
        for friendship in friendships:
            friend_data = {
                'pk': friendship.friend.pk,
                'nickname': friendship.friend.nickname,
                'profile': friendship.friend.profile
            }
            friend_list.append(friend_data)
        return friend_list

    def create_friendship(self, user, friend):
        if user == friend:
            raise serializers.ValidationError({'error': 'You cannot add yourself as a friend'})
        if Friendship.objects.filter(user=user, friend=friend).exists():
            raise serializers.ValidationError({'error': 'You are already friends'})
        friendship = Friendship.objects.create(user=user, friend=friend)
        return friendship

    def delete_friendship(self, user, friend):
        if user == friend:
            raise serializers.ValidationError({'error': 'You cannot delete yourself as a friend'})
        friendship = Friendship.objects.filter(user=user.id, friend=friend.id).first()
        if friendship is None:
            raise serializers.ValidationError({'error': 'You are not friends'})
        friendship.delete()
