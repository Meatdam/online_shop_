from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse

NULABLLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    Расширяет базовую модель таблицы БД Django 'auth_user'
    добавление "image", на выходе имеем таблицу "user_user"
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    image = models.ImageField(upload_to='users_images', **NULABLLE)
    is_verified_email = models.BooleanField(default=False)
    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULABLLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULABLLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class EmailVerification(models.Model):
    """
    Создание модели в БД "EmailVerification", прямая связь с таблицей "User" через "user"
    """
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f' EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        """
        Отправка письма с сылкой для подтверждения учетной записи
        :return: None
        """
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = f'Для завершения регистрации перейдите по ссылке {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        """
        Проверка на истечение срока действия кода
        :return: True or False
        """
        return True if now() >= self.expiration else False
