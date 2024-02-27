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

    def create_superuser(self, email, nickname, **kwargs):
        superuser = self.create_user(
            email,
            nickname,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_admin = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]
    objects = CreateUser()

    def __str__(self):
        return self.email
