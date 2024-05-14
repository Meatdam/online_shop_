from django.contrib import admin

from users.models import User, EmailVerification
from catalog.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Регистрация класса "User" из users/models.py в админ панель
    """
    list_display = ('id', 'username', 'email')
    inlines = (BasketAdmin, )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created_at')
    readonly_fields = ('created_at',)
