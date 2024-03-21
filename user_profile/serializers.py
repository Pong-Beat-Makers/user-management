from rest_framework import serializers
from social_login.serializers import UserSerializer
from social_login.models import User
from friends.models import Friendship
import base64

DEFAULT = False
UPLOAD = True


class ProfileSerializer(UserSerializer):
    profile_to = serializers.BooleanField(source='profile')
    nickname_to = serializers.CharField(source='nickname', max_length=15)
    status_message_to = serializers.CharField(source='status_message', max_length=50, allow_blank=True)
    set_2fa_to = serializers.BooleanField(source='set_2fa')

    class Meta:
        model = User
        fields = ['profile_to', 'nickname_to', 'status_message_to', 'set_2fa_to']

    def get_user_info(self, user, friend):
        is_friend = Friendship.objects.filter(user=user.id, friend=friend.id).exists()

        profile_b64data = ''
        if friend.profile == DEFAULT:
            profile_b64data = 'default'
        elif friend.profile == UPLOAD and friend.uploaded_image is not None:
            profile_b64data = friend.uploaded_image
        else:
            raise serializers.ValidationError({'error': f'{friend.nickname}\'s profile image not found'})

        info = {
            'nickname': friend.nickname,
            'profile': profile_b64data,
            'status_message': friend.status_message,
            'win': friend.win,
            'lose': friend.lose,
            'rank': friend.rank,
            'is_friend': is_friend  # 자기 자신을 조회할 경우 프론트에서 사용되지 않으므로 False여도 상관 없음
        }
        return info

    def update(self, user, validated_data):
        fields = ['profile', 'nickname', 'status_message', 'set_2fa']
        for field in fields:
            value = validated_data.get(field, getattr(user, field))
            if value != getattr(user, field):
                if field == 'profile' and value == UPLOAD and not user.uploaded_image:
                    raise serializers.ValidationError({'error': 'you must upload a profile image first'})
                if field == 'nickname':
                    value = check_nickname(value)
                setattr(user, field, value)
        user.save()
        return user

class ProfileImageSerializer(serializers.Serializer):
    profile_image = serializers.ImageField(required=False, allow_empty_file=True)

    def upload_profile(self, user, validated_data):
        if 'profile_image' in validated_data and validated_data['profile_image'] is not None:
            image_encoded = base64.b64encode(validated_data['profile_image'].read()).decode('utf-8')
            user.uploaded_image = image_encoded
        else:
            user.uploaded_image = None
        user.save()

def check_nickname(nickname):
    if User.objects.filter(nickname=nickname).exists():
        raise serializers.ValidationError({'error': 'This nickname is already in use'})
    return nickname

class RankerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "profile"]
