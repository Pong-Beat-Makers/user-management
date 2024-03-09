from rest_framework import serializers
from social_login.serializers import UserSerializer
from social_login.models import User
from friends.models import Friendship


class ProfileSerializer(UserSerializer):
    profile_to = serializers.CharField(source='profile', max_length=255)
    nickname_to = serializers.CharField(source='nickname', max_length=15)
    status_message_to = serializers.CharField(source='status_message', max_length=50, allow_blank=True)

    class Meta:
        model = User
        fields = ['profile_to', 'nickname_to', 'status_message_to']

    def get_user_info(self, user, friend):
        is_friend = Friendship.objects.filter(user=user.id, friend=friend.id).exists()
        info = {
            'nickname': friend.nickname,
            'profile': friend.profile,
            'status_message': friend.status_message,
            'win': friend.win,
            'lose': friend.lose,
            'rank': friend.rank,
            'is_friend': is_friend  # 자기 자신을 조회할 경우 프론트에서 사용되지 않으므로 False여도 상관 없음
        }
        return info

    def update(self, user, validated_data):
        fields = ['profile', 'nickname', 'status_message']
        for field in fields:
            value = validated_data.get(field, getattr(user, field))
            if value != getattr(user, field):
                if field == 'nickname':
                    value = check_nickname(value)
                setattr(user, field, value)
        user.save()
        return user


def check_nickname(nickname):
    if User.objects.filter(nickname=nickname).exists():
        raise serializers.ValidationError({'error': 'This nickname is already in use'})
    return nickname
