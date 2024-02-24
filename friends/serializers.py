from rest_framework import serializers
from . import models


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friendship
        fields = ('user', 'friend')

    def create_friendship(self, user, friend):
        if user == friend:
            raise serializers.ValidationError('You cannot add yourself as a friend')
        if models.Friendship.objects.filter(user=user, friend=friend).exists():
            raise serializers.ValidationError('You are already friends')

        friendship = models.Friendship.objects.create(user=user, friend=friend)
        return friendship

    def delete_friendship(self, user, friend):
        friendship = models.Friendship.objects.filter(user=user, friend=friend).first()
        if friendship is None:
            raise serializers.ValidationError('You are not friends')
        friendship.delete()
        return friendship
