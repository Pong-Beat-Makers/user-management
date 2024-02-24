from rest_framework import serializers
from social_login.serializers import UserSerializer
from social_login.models import User

class ProfileSerializer(UserSerializer):
    def update(self, user, validated_data):
        user.profile = validated_data.get('profile', user.profile)
        nickname = validated_data.get('nickname')
        if nickname:
            if User.objects.filter(nickname=nickname).exists():
                raise serializers.ValidationError('This nickname is already in use')
            user.nickname = nickname
        user.status_message = validated_data.get('status_message', user.status_message)
        user.save()
        return user
