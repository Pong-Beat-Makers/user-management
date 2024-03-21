import os
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import serializers
from social_login.models import User
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.pagination import PageNumberPagination

class UserProfileView(APIView):
    # 특정유저 조회
    def get(self, request):  # 받는 데이터(query): friend
        try:
            user = request.user
            friend = User.objects.get(nickname=request.GET['friend'])
            serializer = serializers.ProfileSerializer()
            return Response(data=serializer.get_user_info(user, friend), status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': f"friend {request.data['friend']} not found"}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    # 유저 프로필 수정
    def patch(self, request):  # 받는 데이터(Body): profile_to, nickname_to, status_message_to, set_2fa_to
        try:
            user = request.user
            serializer = serializers.ProfileSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.update(user, serializer.validated_data):  # 이미 있는 닉네임인 경우 ValidationError(400) 발생
                    return Response({'message': 'success'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    # 유저 프로필 이미지 업로드
    def post(self, request):
        try:
            user = request.user
            serializer = serializers.ProfileImageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.upload_profile(user, serializer.validated_data)
                return Response({'message': 'success'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class SearchUserView(APIView):  # 받는 데이터(Query): keyword
    # 닉네임으로 유저 검색
    def get(self, request):
        keyword = request.GET['keyword']
        matched_users = User.objects.filter(nickname__icontains=keyword).exclude(nickname=request.user.nickname)
        return Response([{
            'nickname': user.nickname,
            'profile': user.profile,
        } for user in matched_users], status=status.HTTP_200_OK)

class GameRankerView(APIView):
    def get(self, request):
        ranker = User.objects.all().order_by('-rank')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(ranker, request, view=self)
        if page is not None:
            serializer = serializers.RankerUserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = serializers.RankerUserSerializer(ranker, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
