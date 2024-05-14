from django.shortcuts import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User, EmailVerification
from common.views import TitleMixin


class UserLoginView(LoginView):
    """
    Класс для работы с формой "UserLoginForm"
    Отображение полей при логине пользователя и админ панели если пользователь
    является суперпользователем
    """
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    """
    Класс для работы с формой "UserRegistrationForm"
    Отображение полей при регистрации пользователя и админ панели если пользователь
    является суперпользователем
    """
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:email_ver')
    success_message = 'Вы успешно зарегестрировались!'
    title = 'Регистрация'


class ProfileUpdateView(TitleMixin, UpdateView):
    """
    Класс для работы с формой "UserProfileForm"
    Отображение полей при регистрации пользователя и админ панели если пользователь
    является суперпользователем
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Личный кабинет'


class EmailView(TitleMixin, TemplateView):
    """
    Класс для работы с формой "UserRegistrationForm"
    """
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_ver.html'

    def get_success_url(self):
        """
        Функция возвращает url для перенаправления после успешного изменения
        :return: reverse_lazy('users:profile', args=(self.object.id,))
        """
        return reverse_lazy('users:profile', args=(self.object.id,))


def logaut(request):
    """
    Функция вида logaut
    Отображение полей при регистрации пользователя и админ панели если пользователь
    является суперпользователем
    :return: HttpResponseRedirect(reverse('index'))
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin, TemplateView):
    """
    Класс для работы с формой "UserRegistrationForm"
    Отображение полей при регистрации пользователя и админ панели если пользователь
    является суперпользователем
    """
    title = 'YourStore - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))

