from django.urls import path


from bloging.apps import BlogingConfig
from bloging.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, publication

app_name = BlogingConfig.name

urlpatterns = [
    path('create', BlogCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', publication, name='toggle_activity'),
    ]
