from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from catalog.forms import CommentsForm, ProductCreateForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Basket, Version, Category
from catalog.services import get_product_from_cache, get_category_from_cache
from common.views import TitleMixin


class IndexListView(TitleMixin, ListView):
    """
    Класс для отображения списка товаров
    model = Product
    paginate_by = 6
    title = 'Главная'
    """
    model = Product
    paginate_by = 8
    title = 'Главная'

    def get_queryset(self):
        """
        Переопределяем метод get_queryset для фильтрации товаров по категории
        поключен кеш к queryset services/get_product_from_cach
        :param: category_id
        :return: queryset
        """
        queryset = get_product_from_cache()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *args, **kwargs):
        """
        Добавление категорий в контекст
        подключен кеш services/get_category_from_cach
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return: context_data['categories']
        """
        context_data = super().get_context_data(*args, **kwargs)
        context_data['categories'] = get_category_from_cache()
        return context_data


class ContactsView(TitleMixin, TemplateView):
    """
    Класс для отображения страницы контактов
    model = Product
    title = 'Контакты'
    """
    template_name = 'catalog/contacts.html'
    title = 'Контакты'


class ProductDetailView(FormMixin, DetailView):
    """
    Класс для отображения страницы товара
    model = Product
    """
    model = Product
    form_class = CommentsForm
    title = 'Описание товара'

    def get_success_url(self, **kwargs):
        """
        Переопределение метода "get_success_url" для перехода на страницу товара
        :return: reverse_lazy('catalog:single_product', kwargs={'pk': self.get_object().id})
        """
        return reverse_lazy('catalog:single_product', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        """
        Переопределение метода "post" для сохранения комментария
        :param: request
        :param: *args
        :param: **kwargs
        :return: super().post(request, *args, **kwargs)
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Переопределение метода "form_valid" для сохранения комментария
        :param: form
        :return: super().form_valid(form)
        """
        self.object = form.save(commit=False)
        self.object.product = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductCreateView(TitleMixin, CreateView):
    """
    Класс для отображения страницы создания товара
    """
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('catalog:index')
    title = 'Создание товара'

    def get_context_data(self, **kwargs):
        """
        Переопределение метода "get_context_data" для отображения формы
        :param: **kwargs
        :return: context_data
        """
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        return context_data

    def form_valid(self, form):
        """
        Привязывает продукт к текущему пользователю.
        """
        product = form.save()
        product.user_owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, TitleMixin, UpdateView):
    """
    Класс для отображения страницы редактирования товара
    """
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('catalog:index')
    title = 'Редактирование товара'

    def get_context_data(self, **kwargs):
        """
        Переопределение метода "get_context_data" для отображения формы
        :param: **kwargs
        :return: context_data
        """
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        Переопределение метода "form_valid" для сохранения слага
        :param: form
        :return: super().form_valid(form)
        """
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        """
        Проверка на владельца продукта или модератора с правами на редактирование
        """
        user = self.request.user
        if user == self.object.user_owner:
            return ProductCreateForm
        if (user.has_perm('catalog.can_edit_publication_sign') and user.has_perm('catalog.can_edit_category')
                and user.has_perm('catalog.can_edit_description')):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(TitleMixin, DeleteView):
    """
    Класс для отображения страницы удаления товара
    """
    model = Product
    title = 'Удаление товара'
    success_url = reverse_lazy('catalog:index')


@login_required
def basket_add(request, product_id):
    """
    Функция добавления товара в корзину
    :param: request
    :param: product_id
    :return: HttpResponseRedirect(request.META['HTTP_REFERER'])
    """
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    """
    Функция удаления товара из корзины
    :param: request
    :param: basket_id
    :return: HttpResponseRedirect(request.META['HTTP_REFERER'])
    """
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
