from rest_framework.generics import ListAPIView
from .serializers import CategoryModelSerializer, UnderCategoryModelSerializers, ProductModelSerializers
from main.models import Category, UnderCategory, Product


class CategoryApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UnderCategoryApi(ListAPIView):
    queryset = UnderCategory.objects.all()
    serializer_class = UnderCategoryModelSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductApi(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)