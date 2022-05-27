from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from embed_video.fields import EmbedVideoField


class User(AbstractUser):
    """Переопределение USER, логин по почте """
    email = models.EmailField(_('email address'), unique=True)
    tel = models.CharField(max_length=11, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UnderCategory(models.Model):
    """M-2-O Подкатегории товаров"""
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, default='', editable=False)

    class Meta:
        ordering = ("slug",)
        verbose_name = "UnderCategory"
        verbose_name_plural = "UndreCategories"

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)  # поле может принимать Unicode символы кроме ASCII
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:product_list_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Category(models.Model):
    """M-2-O Категории товаров"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, default='', editable=False)
    under_category = models.ForeignKey(UnderCategory, related_name="under_products", on_delete=models.CASCADE)

    class Meta:
        ordering = ("under_category",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)  # поле может принимать Unicode символы кроме ASCII
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:product_list_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name},{self.under_category}"


class Brand(models.Model):
    """ M-2-M Бренд товора"""
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, default='',
                            editable=False)  # editable не отображать в админке,пропускается валидация

    class Meta:
        ordering = ("slug",)
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Bazar(models.Model):
    """Магазины"""
    name = models.CharField(max_length=200, db_index=True, unique=True)
    adress = models.CharField(max_length=200, unique=True)
    tel = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.name},{self.adress},{self.tel}"


class Tag(models.Model):
    """M-2-O Тэг по категориям товаров"""
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, default='', editable=False)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    """M-2-O Подкатегории товаров"""
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Основной класс Product"""
    Product_Availability = (
        ('Y', 'Есть в наличии'),
        ('N', 'Нет в наличии'),
        ('S', 'Не производится'),
        ('Z', 'Ожидается поступление'),
    )
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, default='', editable=False)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    bazar = models.ForeignKey(Bazar, related_name="bazars", on_delete=models.CASCADE)
    brand = models.ManyToManyField(Brand, related_name="brands")
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    video_new = EmbedVideoField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    price_old = models.DecimalField(max_digits=8, decimal_places=2)
    articles = models.ForeignKey(Article, related_name="articles", on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=Product_Availability, default='Y')
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    tag = models.ForeignKey(Tag, related_name="tags", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name},{self.category}"


class TwiceProduct(models.Model):
    """Модель двойных товаров"""
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, editable=False)
    products = models.ManyToManyField(Product, related_name="tw_product")
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name}"
