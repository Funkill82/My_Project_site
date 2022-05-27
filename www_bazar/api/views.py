from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from .serializers import CategoryModelSerializer, UnderCategoryModelSerializers, ProductModelSerializers, \
    ProductDetailModelSerializers
from main.models import Category, UnderCategory, Product, Brand


class CategoryApi(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (IsAdminUser,)


class UnderCategoryApi(ListAPIView):
    queryset = UnderCategory.objects.all()
    serializer_class = UnderCategoryModelSerializers
    permission_classes = (IsAdminUser,)


class ProductApi(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializers

    @action(methods=['get'], detail=False)
    def brand(self, request):
        brands = Brand.objects.all()
        return Response({'brands': [x.name for x in brands]})

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        categorys = Category.objects.get(pk=pk)
        return Response({'brands': categorys.name})
