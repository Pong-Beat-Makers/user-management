| 앱 이름 | 뷰 명칭 | 요청 타입 | 기능 설명 | 요청 데이터 타입 | 요구 데이터 | 응답 데이터 | 응답 형식 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| social_login | SocialLogin | GET | 소셜로그인 URL 세팅 |  |  | 로그인 URL |  |
|  | SocialLoginCallBack | GET | 액세스 토큰과 리프레시 토큰 발행, 쿠키 세팅 |  |  | 프론트엔드 URL |  |
| friends | FriendshipView | GET | 사용자의 친구목록 반환 |  |  | 각 친구당 pk, 닉네임, 프로필 | {“pk”: “1”,”nickname”: “user 1”,”profile”: “default”} |
|  |  | POST | 친구 추가 | HTTP 본문 | friend(pk) | 성공/에러 메세지 | {"success":"1st user added 2nd user as a friend"} |
|  |  | DELETE | 친구 삭제 | URL 파라미터 | friends/<int:user_pk>/delete/<int:friend_pk> | 성공/에러 메세지 | {"success":"1st user deleted friend 2nd user"} |
| user_profile | UserProfileView | GET | 특정 유저 조회 | Query | friend(pk) | 닉네임, 프로필, 상태메세지, 승, 패, 랭크, 친구여부 | {"nickname":"user1","profile":"default","status_message":"Hello","win":1,"lose":1,"rank":4,"is_friend":False} |
|  |  | PATCH | 유저 프로필 수정 | HTTP 본문 | profile_to, nickname_to, status_message_to | 성공/에러 메세지 | {"message":"success"} |
|  | SearchUserView | GET | 닉네임으로 유저 검색 | Query | keyword | 필터링된 유저들의 닉네임 목록 | [”1st user”,”2nd user”] |

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
# API Specification
***
## 구글 로그인
***
### 접속
#### http method : GET
#### path: /accounts/google/login/
***
### 응답예시
#### 형식 : json
***
### 성공
#### status code : 200 OK
#### 1. 이미 로그인 되어 있는 경우
<pre>
<code>
{
    "error": "already logged in"
}
</code>
</pre>
***
#### 2. 정상적으로 회원가입/로그인이 되었을 경우
<pre>
<code>
{
    "user": "< 유저 구글 이메일 >",
    "message": "Logged in successfully",
    "refresh": "< refresh 토큰 >",
    "access": "< access 토큰 >"
}
</code>
</pre>
***
### 실패 
#### status code : 400 BAD REQUEST
#### 1. 구글 api에서 code를 발급 받지 못했을 경우
<pre>
<code>
{
    "error": "code is required"
}
</code>
</pre>
#### 2. 구글 api에서 받은 code가 유효하지 않을 경우
<pre>
<code>
{
    "error": "invalid code"
}
</code>
</pre>
***
## 42 로그인
***
### 접속
#### http method : GET
#### path: /accounts/42intra/login/
***
### 응답예시
#### 형식 : json
***
### 성공
#### status code : 200 OK
#### 1. 이미 로그인 되어 있는 경우
<pre>
<code>
{
    "error": "already logged in"
}
</code>
</pre>
***
#### 2. 정상적으로 회원가입/로그인이 되었을 경우
<pre>
<code>
{
    "user": "< 유저 42 이메일 >",
    "message": "Logged in successfully",
    "refresh": "< refresh 토큰 >",
    "access": "< access 토큰 >"
}
</code>
</pre>
***
### 실패 
#### status code : 400 BAD REQUEST
#### 1. 42 api에서 code를 발급 받지 못했을 경우
<pre>
<code>
{
    "error": "code is required"
}
</code>
</pre>
#### 2. 42 api에서 받은 code가 유효하지 않을 경우
<pre>
<code>
{
    "error": "invalid code"
}
</code>
</pre>
