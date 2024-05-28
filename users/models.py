from django.db import models
from django.contrib.auth.models import AbstractUser


NULABLLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    Расширяет базовую модель таблицы БД Django 'auth_user'
    добавление "image", на выходе имеем таблицу "user_user"
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    image = models.ImageField(upload_to='users_images', **NULABLLE)
    verification_code = models.CharField(max_length=30, **NULABLLE)
    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULABLLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULABLLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
