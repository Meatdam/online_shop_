import string
import random

from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from config.settings import EMAIL_HOST_USER
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
    success_url = reverse_lazy('users:profile')

    def get_success_url(self, **kwargs):
        """
        Переопределение метода "get_success_url" для перехода на страницу товара
        :return: reverse_lazy('catalog:single_product', kwargs={'pk': self.get_object().id})
        """
        return reverse_lazy('users:profile', kwargs={'pk': self.get_object().id})


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


def reset_password(request):
    context = {
        'success_message': 'Пароль успешно сброшен. Новый пароль был отправлен на ваш адрес электронной почты.',
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        characters = string.ascii_letters + string.digits
        characters_list = list(characters)
        random.shuffle(characters_list)
        password = ''.join(characters_list[:10])

        # user.set_password(make_password(password))
        user.set_password(password)
        user.save()

        send_mail(
            subject='Восстановление пароля',
            message=f'Здравствуйте, вы запрашивали обновление пароля. Ваш новый пароль: {password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return render(request, 'users/reset_password.html', context)

    return render(request, 'users/reset_password.html')

