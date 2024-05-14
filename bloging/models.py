from django.db import models
from django.utils import timezone

from users.models import User

NULABLLE = {'null': True, 'blank': True}


class Blog(models.Model):
    """
    Создание модели в БД "Blog", прямая связь с таблицей "User" через "user"
    """
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.CharField(max_length=255, verbose_name='Слаг', **NULABLLE)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='blog', verbose_name='Изображение', **NULABLLE)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    publication_sign = models.BooleanField(default=True, verbose_name='Опубликован')
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='владелец', **NULABLLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
