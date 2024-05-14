from django.contrib import admin

from bloging.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Регистрация класса "User" из users/models.py в админ панель
    """
    list_display = ('title', 'description', 'image', 'created_at', 'publication_sign',)
