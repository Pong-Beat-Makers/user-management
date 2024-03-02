# user-management
drf를 이용한 유저 회원가입과 로그인, 유저관련 db 처리
***
# 환경
* ### Python 3.11
* ### Django 5.0.1
***
# 실행방법
<pre>
<code>
pip install -r requirements.txt
python manage.py makemigrations social_login
python manage.py migrate social_login
python manage.py runserver
</code>
</pre>
***
# 사용
사용법 총 정리 테이블은 본문 하단 참조
### URL별 기능
+ `accounts/<social>/login` - 소셜로그인 URL 세팅
    * GET
+ `accounts/<social>/login/callback` - 토큰 발행 및 쿠키 세팅
    * GET
+ `friends/` - 친구목록, 친구추가
    * GET
    * POST: Body: `friend`(pk)
+ `friends/<int:user_pk>/delete/<int:friend_pk>` - 친구삭제
    * DELETE
+ `profile/` - 유저조회, 프로필 수정
    * GET: Query: `friend`(pk)
    * PATCH: Body: `profile_to`, `nickname_to`, `status_message_to`
+ `profile/search/` - 유저 검색
    * GET: Query: `keyword`
***
# USUAGE TABLE
| 앱 이름 | 뷰 명칭 | URL | 요청 타입 | 기능 설명 | 요청 데이터 타입 | 요구 데이터 | 응답 데이터 | 응답 형식 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `social_login` | `SocialLogin` | `accounts/<social>/login/` | GET | 소셜로그인 URL 세팅 |  |  | 로그인 URL |  |
|  | `SocialLoginCallBack` | `accounts/<social>/login/callback` | GET | 액세스 토큰과 리프레시 토큰 발행, 쿠키 세팅 |  |  | 프론트엔드 URL |  |
| `friends` | `FriendshipView` | `friends/` | GET | 사용자의 친구목록 반환 |  |  | 각 친구당 pk, 닉네임, 프로필 | `{“pk”: “1”,”nickname”: “user 1”,”profile”: “default”}` |
|  |  |  | POST | 친구 추가 | HTTP 본문 | `friend`(pk) | 성공/에러 메세지 | `{"success":"1st user added 2nd user as a friend"}` |
|  |  | `friends/<int:user_pk>/delete/<int:friend_pk>` | DELETE | 친구 삭제 | URL 파라미터 | user pk, friend pk | 성공/에러 메세지 | `{"success":"1st user deleted friend 2nd user"}` |
| `user_profile` | `UserProfileView` | `profile/` | GET | 특정 유저 조회 | Query | `friend`(pk) | 닉네임, 프로필, 상태메세지, 승, 패, 랭크, 친구여부 | `{"nickname":"user1","profile":"default","status_message":"Hello","win":1,"lose":1,"rank":4,"is_friend":False}` |
|  |  |  | PATCH | 유저 프로필 수정 | HTTP 본문 | `profile_to`, `nickname_to`, `status_message_to` | 성공/에러 메세지 | `{"message":"success"}` |
|  | `SearchUserView` | `profile/search/` | GET | 닉네임으로 유저 검색 | Query | `keyword` | 필터링된 유저들의 닉네임 목록 | `[”1st user”,”2nd user”]` |
