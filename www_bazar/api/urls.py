from django.urls import path
from .views import CategoryApi, UnderCategoryApi, ProductApi

app_name = "api"

urlpatterns = [

    path('category/', CategoryApi.as_view(), name='category'),
    path('undercategory/', UnderCategoryApi.as_view(), name='undercategory'),
    path('product/', ProductApi.as_view(), name='product'),

]