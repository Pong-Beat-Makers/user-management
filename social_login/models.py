from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CreateUser(BaseUserManager):
    def create_user(self, email, nickname, **kwargs):
        if not nickname:
            raise ValueError('Please write your nickname')
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nickname = models.CharField(
        max_length=15,
        unique=True,
    )
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    profile = models.CharField(default='default', max_length=255)
    status_message = models.CharField(default='', max_length=50, null=False, blank=True)
    email_verification_code = models.CharField(max_length=6, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]
    objects = CreateUser()

    def __str__(self):
        return self.email
