from rest_framework import serializers
from main.models import Category, UnderCategory, Product, Brand, Bazar


class UnderCategoryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = UnderCategory
        fields = ['name']


class CategoryModelSerializer(serializers.ModelSerializer):
    under_category = UnderCategoryModelSerializers()
    class Meta:
        model = Category
        fields = ['name', 'under_category']


class BrandModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class BazarModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bazar
        fields = ['name']

class ProductModelSerializers(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    undercategory_name = serializers.CharField(source='category.under_category.name')
    brand = BrandModelSerializers(many=True)
    bazar_name = serializers.CharField(source='bazar.name')
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "price_old", "stock", "available",
                  "category_name", "undercategory_name", "bazar_name", "brand"]






