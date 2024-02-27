from rest_framework import serializers
from social_login.serializers import UserSerializer
from social_login.models import User


class ProfileSerializer(UserSerializer):
    profile_to = serializers.CharField(source='profile', max_length=255)
    nickname_to = serializers.CharField(source='nickname', max_length=15)
    status_message_to = serializers.CharField(source='status_message', max_length=50, allow_blank=True)

    class Meta:
        model = User
        fields = ['profile_to', 'nickname_to', 'status_message_to']

    def update(self, user, validated_data):
        fields = ['profile', 'nickname', 'status_message']
        for field in fields:
            value = validated_data.get(field, getattr(user, field))
            if value != getattr(user, field):
                if field == 'nickname':
                    value = self.check_nickname(value)
                setattr(user, field, value)
        user.save()
        return user

    def check_nickname(self, nickname):
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError({'error': 'This nickname is already in use'})
        return nickname
