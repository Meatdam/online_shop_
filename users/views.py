import string
import random

from django.core.management import settings
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from config.settings import EMAIL_HOST_USER
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    """
    Класс для работы с формой "UserLoginForm"
    Отображение полей при логине пользователя и админ панели если пользователь
    является суперпользователем
    """
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'


class UserRegistrationCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    """
    Класс для работы с формой "UserRegistrationForm"
    Отображение полей при регистрации пользователя и админ панели если пользователь
    является суперпользователем
    """
    model = User
    form_class = UserRegistrationForm
    success_message = 'Вы успешно зарегестрировались!'
    title = 'Регистрация'

    def form_valid(self, form):

        user = form.save()
        user.is_active = False

        verification_code = ''.join([str(random.randint(1, 9)) for _ in range(8)])
        user.verification_code = verification_code

        current_site = self.request.get_host()
        subject = 'Подтверждение регистрации'
        message = (f'Для завершения регистрации перейдите по ссылке:\n {current_site}/users/confirm\n '
                   f'Код для регистрации: {verification_code}')

        user.save()
        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:confirm')


class ConfirmRegister(TitleMixin, TemplateView):
    """
    Класс для подтверждения электроной почты
    проверка пользователя на введение корректного кода регистрации
    """
    title = 'Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        return render(request, 'users/register_confirm.html')

    def post(self, request, *args, **kwargs):
        token = int(request.POST.get('verification_code'))
        user = get_object_or_404(User, verification_code=token)

        if not user.is_active:
            user.is_active = True
            user.save()
            return render(request, 'users/email_verification.html')
        return redirect('catalog:index')


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


def logaut(request):
    """
    Функция вида logaut
    Отображение полей при регистрации пользователя и админ панели если пользователь
    является суперпользователем
    :return: HttpResponseRedirect(reverse('index'))
    """
    auth.logout(request)
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

