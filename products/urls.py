from django.urls import path
from .views import add_product, product_list, get_products_json

urlpatterns = [
    path('add/', add_product, name='add_product'),
    path('', product_list, name='product_list'),
    path('json/', get_products_json, name='get_products_json'),
]
