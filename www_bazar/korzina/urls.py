# from django.urls import re_path as url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "korzina"



urlpatterns = [
    path('korzina/', views.korzina_detail, name='korzina_detail'),
    path('korzina_add/<int:product_id>', views.korzina_add, name='korzina_add'),
    path('korzina_tw_add/<int:product_id>', views.korzina_tw_add, name='korzina_tw_add'),
    path('korzina_remove/<int:product_id>', views.korzina_remove, name='korzina_remove'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)