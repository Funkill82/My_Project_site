from django.urls import path

from .views import order_create, kupon_activate, order_create_one_click

app_name = "orders"

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('create_1click/', order_create_one_click, name='create_1click'),
    path('kupon/', kupon_activate, name='kupon_activate'),
]