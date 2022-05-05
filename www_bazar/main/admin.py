from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from  embed_video.admin  import  AdminVideoMixin

from .models import UnderCategory, Category, Brand, Bazar, Tag, Product, Article, TwiceProduct

User = get_user_model()
@admin.register(User)
class UserAdmin(UserAdmin):
    pass
@admin.register(UnderCategory)
class UnderCategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(Bazar)
class BazarAdmin(admin.ModelAdmin):
    pass
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
@admin.register(Product)
class ProductAdmin(AdminVideoMixin,admin.ModelAdmin):
    pass

@admin.register(TwiceProduct)
class TwiceProductAdmin(admin.ModelAdmin):
    pass
