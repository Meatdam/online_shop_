from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from pytils.translit import slugify
from django.contrib.auth.mixins import LoginRequiredMixin

from bloging.forms import AddBlogForm
from bloging.models import Blog
from common.views import TitleMixin


class BlogCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    """
    Регистрация класса "Blog" из bloging/models.py в админ панель
    """
    model = Blog
    form_class = AddBlogForm
    success_url = reverse_lazy('bloging:list')
    title = 'Создание отзыва'

    def form_valid(self, form):
        """
        Переопределение метода "form_valid" для сохранения слага
        """

        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = self.request.user
            new_blog.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogListView(TitleMixin, ListView):
    """
    Регистрация класса "Blog" из bloging/models.py в админ панель
    """
    model = Blog
    title = 'Отзывы'

    def get_queryset(self, *args, **kwargs):
        """
        Переопределение метода "get_queryset" для фильтрации отзывов
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication_sign=True)
        return queryset


class BlogDetailView(TitleMixin, DetailView):
    """
    Регистрация класса "Blog" из bloging/models.py в админ панель
    """
    model = Blog
    title = 'Отзыв'

    def get_object(self, queryset=None):
        """
        Переопределение метода "get_object" для фильтрации отзывов
        :return: get_object_or_404(Blog, slug=self.kwargs.get('slug'))
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, TitleMixin, UpdateView):
    """
    Класс для редактирования отзыва
    """
    model = Blog
    title = 'Редактирование отзыва'
    form_class = AddBlogForm

    def form_valid(self, form):
        """
        Переопределение метода "form_valid" для сохранения слага
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Переопределение метода "get_success_url" для перехода на страницу отзыва
        :return: reverse('bloging:view', args=[self.kwargs.get('pk')])
        """
        return reverse('bloging:view', args=[self.kwargs.get('pk')])

    def get_form_kwargs(self):
        """
        Переопределение метода "get_form_class" для фильтрации отзывов
        :return: AddBlogForm
        """
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].owner:
            return self.handle_no_permission()
        return kwargs


class BlogDeleteView(LoginRequiredMixin, TitleMixin, DeleteView):
    """
    Удаление отзыва
    """
    model = Blog
    title = 'Удаление отзыва'
    success_url = reverse_lazy('bloging:list')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        if self.request.user != self.object.owner:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def publication(request, pk):
    """
    Функция для публикации отзыва
    :param request:
    :param pk:
    :return: redirect(reverse('bloging:list'))
    """
    publication_item = get_object_or_404(Blog, pk=pk)
    if publication_item.publication_sign:
        publication_item.publication_sign = False
    else:
        publication_item.publication_sign = True

    publication_item.save()
    return redirect(reverse('bloging:list'))
