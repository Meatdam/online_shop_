from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    """
    Создание модели в БД "Category", прямая связь с таблицей "Product" через "category"
    """
    name = models.CharField(max_length=250, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """
    Создание модели в БД "Product", прямая связь с таблицей "Category" через "category"
    """
    name = models.CharField(max_length=250, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    avatar = models.ImageField(upload_to='catalog/', verbose_name='аватар', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.FloatField(verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='дата создания')
    updated_at = models.DateTimeField(verbose_name='дата изменения', **NULLABLE)

    def __str__(self):
        return f"{self.name} ({self.price})"

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Carousel(models.Model):
    """
    Создание модели в БД "Carousel" связи отсутствуют
    """
    name = models.CharField(max_length=150, verbose_name='Название')
    images = models.ImageField(upload_to='catalog/carusel', verbose_name='слайд')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'слайд'
        verbose_name_plural = 'слайды'


class BasketQuerySet(models.QuerySet):
    """
    Класс подсчета общей суммы в корзине
    и подсчета количества товаров лежащих в корзине
    """
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    """
    Создание модели в БД "Basket", прямая связь с таблицей "User" через "user"
    и прямая связь "Product" через "product"
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user} | Продукт: {self.product.name}"

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def sum(self):
        return self.product.price * self.quantity


class Comments(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='продукт', **NULLABLE,
                                related_name='comments_product')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='автор комментария', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    text = models.TextField(verbose_name='текст комментария')
    status = models.BooleanField(default=False, verbose_name='видимость комментария')


class Version(models.Model):
    """
    Создание модели в БД "Version", прямая связь с таблицей "Product" через "product"
    """
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='продукт')
    number_version = models.IntegerField(default=1, verbose_name='номер версии')
    version_name = models.CharField(max_length=250, verbose_name='название версии')
    version_flag = models.BooleanField(default=True, verbose_name='признак версии')

    def __str__(self):
        return f"{self.number_version}: {self.version_name}"

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ['number_version']
