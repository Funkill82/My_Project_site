from rest_framework import generics, viewsets
from rest_framework.generics import ListAPIView
from .serializers import CategoryModelSerializer, UnderCategoryModelSerializers, ProductModelSerializers, \
    ProductDetailModelSerializers
from main.models import Category, UnderCategory, Product


class CategoryApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class UnderCategoryApi(ListAPIView):
    queryset = UnderCategory.objects.all()
    serializer_class = UnderCategoryModelSerializers


class ProductApi(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializers


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =  ProductDetailModelSerializers
