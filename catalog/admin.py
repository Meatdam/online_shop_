from django.contrib import admin

from catalog.models import Category, Product, Carousel, Basket, Comments, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Регистрация класса "Category" из models.py в админ панель
    """
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Регистрация класса "Product" из catalog/models.py в админ панель
    """
    list_display = ('id', 'name', 'price', 'quantity', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)
    ordering = ('name',)


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    """
    Регистрация класса "Carousel" из models.py в админ панель
    """
    list_display = ('id', 'name')


class BasketAdmin(admin.TabularInline):
    """
    Ругистрация класса "Basket" из models.py в админ панель
    """
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'created_at', 'text', 'status')
    list_filter = ('user', )


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('number_version', 'version_name', 'version_flag',)
    list_filter = ('version_name', )

