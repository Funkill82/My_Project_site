from django.urls import path, include
from rest_framework import routers

from .views import CategoryApi, UnderCategoryApi, ProductViewSet

app_name = "api"

router = routers.SimpleRouter()

router.register(r'product', ProductViewSet)


urlpatterns = [

    path('v1/category/', CategoryApi.as_view(), name='category'),
    path('v1/undercategory/', UnderCategoryApi.as_view(), name='undercategory'),
    path('v1/', include(router.urls)),
    # path('v1/product/', ProductApi.as_view(), name='product'),
    # path('v1/product_detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),

]