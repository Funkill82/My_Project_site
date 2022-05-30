from django.urls import path, include
from .views import Register, CategoryList, UnderCategoryList, ProductDetail, \
    sort_filter, SearchView, TopProductList, WeekSaleProductList, TwiceProductList
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

app_name = "main"

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('category_list/<str:slug>', CategoryList.as_view(), name='category_list'),
    path('products/<str:slug>', UnderCategoryList.as_view(), name='product_list_by_category'),
    path('product/<str:slug>', ProductDetail.as_view(), name='product_detail'),
    path('search/>', SearchView.as_view(), name='search_results'),
    path('filter/', sort_filter, name='filter'),
    path('top/', cache_page(180)(TopProductList.as_view()), name='top'),
    path('week_sale/', cache_page(180)(WeekSaleProductList.as_view()), name='week_sale'),
    path('twice_product/', cache_page(180)(TwiceProductList.as_view()), name='twice_product'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
