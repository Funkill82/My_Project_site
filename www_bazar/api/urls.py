from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from .views import CategoryApi, UnderCategoryApi, ProductViewSet

app_name = "api"

router = routers.SimpleRouter()

router.register(r'product', ProductViewSet)


urlpatterns = [

    path('v1/category/', CategoryApi.as_view(), name='category'),
    path('v1/undercategory/', UnderCategoryApi.as_view(), name='undercategory'),
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('v1/product/', ProductApi.as_view(), name='product'),
    # path('v1/product_detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),

]