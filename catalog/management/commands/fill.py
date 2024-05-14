import json
from pprint import pprint

from catalog.models import Product, Category
from config.settings import BASE_DIR

from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Класс кастомной команды для заполнения Форм БД "product"
    """

    @staticmethod
    def json_read_categories() -> list:
        """
        Метод забирает данные из json файла (данные для базы данных "category")
        и склабываем в список "list_category"
        :return: List
        """
        list_category = []
        with open(BASE_DIR / 'data.json') as file:
            categoryes = json.load(file)
            for category in categoryes:
                if category["model"] == "catalog.category":
                    list_category.append(category)
            return list_category

    @staticmethod
    def json_read_products() -> list:
        """
        Метод забирает данные из json файла (данные для базы данных "product")
        и склабываем в список "list_products"
        :return: List
        """
        list_products = []
        with open(BASE_DIR / 'data.json') as file:
            products = json.load(file)
            for product in products:
                if product["model"] == "catalog.product":
                    list_products.append(product)
            return list_products

    def handle(self, *args, **options):
        """
        Функция удаления старых данных из таблиц, и заполнение новыми данными
        """
        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(
                Category(id=category["pk"],
                         name=category["fields"]["name"],
                         description=category["fields"]["description"])
            )
        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(
                Product(id=product["pk"],
                        name=product["fields"]["name"],
                        description=product["fields"]["description"],
                        quantity=product["fields"]["quantity"],
                        category=Category.objects.get(pk=product["fields"]["category"]),
                        price=product["fields"]["price"])
            )
        Product.objects.bulk_create(product_for_create)
