import uuid
from datetime import timedelta

from django import forms
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from common.views import StyleFormMixin
from users.models import User, EmailVerification


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Класс для работы с формой "UserLoginForm"
    """
    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegistrationForm(StyleFormMixin, UserCreationForm):
    """
    Класс для работы с формой "UserRegistrationForm"
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """
        Переопределение метода "save" для создания записи в таблице "EmailVerification"
        :param commit:
        :return:
        """
        user = super(UserRegistrationForm, self).save(commit=True)
        expiretion = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiretion)
        record.send_verification_email()
        return user


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
    Класс для работы с формой "UserProfileForm"
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'email', 'phone', 'country')
