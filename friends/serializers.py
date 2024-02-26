from rest_framework import serializers
from . import models


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friendship
        fields = '__all__'

    def create_friendship(self, user, friend):
        if user == friend:
            raise serializers.ValidationError({'error': 'You cannot add yourself as a friend'})
        if models.Friendship.objects.filter(user=user, friend=friend).exists():
            raise serializers.ValidationError({'error': 'You are already friends'})

        friendship = models.Friendship.objects.create(user=user, friend=friend)
        return friendship
