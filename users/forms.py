from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from common.views import StyleFormMixin
from users.models import User


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


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
    Класс для работы с формой "UserProfileForm"
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'email', 'phone', 'country')
