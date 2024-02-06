# from django.dispatch import receiver
# from allauth.socialaccount.signals import social_account_added
# from django.contrib.auth import get_user_model

# @receiver(social_account_added)
# def social_login_success_handler(sender, request, sociallogin, **kwargs):
#     # 소셜 로그인을 통해 받아온 사용자 정보
#     social_user_info = {
#         'email': sociallogin.user.email,
#         'nickname': sociallogin.account.extra_data.get('nickname'),
#         'profile_image_url': sociallogin.account.extra_data.get('profile_image_url'),
#         # 필요한 다른 정보들...
#     }

#     # 커스텀 유저 모델 가져오기
#     User = get_user_model()

#     # 사용자 정보 추출 및 저장
#     user, created = User.objects.get_or_create(email=social_user_info['email'])
#     user.nickname = social_user_info['nickname']
#     user.profile_image_url = social_user_info['profile_image_url']
#     # 필요한 다른 필드에 대한 처리...

#     # 변경사항 저장
#     user.save()
# from django.contrib.auth import get_user_model

# User = get_user_model()

# # createsuperuser를 통해 슈퍼유저 생성
# superuser = User.objects.create_superuser('elinlim22@gmail.com', 'dummy_password')

# # 더미 비밀번호로 슈퍼유저 생성
# superuser.set_unusable_password()

# # 슈퍼유저 저장
# superuser.save()

