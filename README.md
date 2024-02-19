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