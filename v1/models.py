from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from v1.common_utils.managers import get_manager
from django.contrib.auth.models import BaseUserManager
import secrets
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin, BaseUserManager):
    email = models.EmailField(max_length=150, blank=True, null=True, verbose_name='Почта')
    username = models.EmailField(max_length=150, unique=True, verbose_name='Имя пользователя')
    password = models.CharField(max_length=150, verbose_name='Пароль')
    token = models.CharField(max_length=256, default=secrets.token_hex(128), verbose_name='Токен')
    is_staff = models.BooleanField(default=False, null=True)
    is_superuser = models.BooleanField(default=0, null=True)
    is_active = models.BooleanField(default=1, null=True)
    is_official = models.BooleanField(default=False, null=True)
    USERNAME_FIELD = 'username'

    objects = get_manager('user')

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Categories(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    category = models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    create_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статья'


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE, verbose_name='Статья')
    content = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    create_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
