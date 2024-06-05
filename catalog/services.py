from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_product_from_cache():
    """
    Получает данные по товарам из кэша,
    если кэш пуст - получает данные из БД.
    """
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = 'product_list'
    product = cache.get(key)
    if product is not None:
        return product
    product = Product.objects.all()
    cache.set(key, product)
    return product


def get_category_from_cache():
    """
    Получает данные по категориям из кэша,
    если кэш пуст - получает данные из БД.
    """
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = 'category_list'
    category = cache.get(key)
    if category is not None:
        return category
    category = Category.objects.all()
    cache.set(key, category)
    return category



