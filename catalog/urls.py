from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import IndexListView, basket_add, basket_remove, ProductDetailView, ContactsView, ProductCreateView, \
    ProductDeleteView, ProductUpdateView
from catalog.apps import CatalogConfig


app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('page/<int:page>/', IndexListView.as_view(), name='paginator'),
    path('category/<int:category_id>/', cache_page(60)(IndexListView.as_view()), name='category'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='single_product'),
    path('contacts/', cache_page(60)(ContactsView.as_view()), name='contacts'),
    path('create/', ProductCreateView.as_view(), name='create')
]
