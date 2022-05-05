from django.contrib.auth import authenticate, login
from django.views import generic
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from .forms import UserCreationForm, SortFilterForm
from .models import Category, Product, TwiceProduct
from korzina.forms import KorzinaAddProductForm
from django.db.models import Q, F


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {'form': UserCreationForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        context = {'form': form}
        return render(request, self.template_name, context)


class CategoryList(generic.ListView):
    """Таблица категорий"""
    model = Category
    template_name = 'category_list.html'
    sort_form = SortFilterForm()
    extra_context = {'sort_form': sort_form}
    paginate_by = 10

    def get_queryset(self):
        return Category.objects.filter(slug__exact=self.kwargs['slug'])


class UnderCategoryList(generic.ListView):
    """Таблица под-категорий"""
    model = Product
    template_name = 'product_list_by_category.html'
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(category__under_category__slug=self.kwargs['slug'], available=True)


class TopProductList(generic.ListView):
    """Таблица топ продаж"""
    model = Product
    template_name = 'top_product.html'
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(stock__lte=15, available=True)


class WeekSaleProductList(generic.ListView):
    """Таблица товара со скидками за неделю"""
    model = Product
    template_name = 'week_sale.html'
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(price_old__gt=F("price"))


class ProductDetail(DetailView):
    """Детальное описание продукта"""
    model = Product
    korzina_product_form = KorzinaAddProductForm()
    extra_context = {'korzina_product_form': korzina_product_form}



class TwiceProductList(generic.ListView):
    """Таблица комплектов"""
    model = TwiceProduct
    template_name = 'twice_product_list.html'
    korzina_product_form = KorzinaAddProductForm()
    extra_context = {'korzina_product_form': korzina_product_form}
    paginate_by = 1


def sort_filter(request):
    """Обработка фильтра"""
    form = SortFilterForm()
    if request.method == 'POST':
        form = SortFilterForm(request.POST)
        if form.is_valid():
            categorys = form.cleaned_data.get('category')
            brands = form.cleaned_data.get('brand')
            bazars = form.cleaned_data.get('bazar')
            prices_min = form.cleaned_data.get('price_min')
            prices_max = form.cleaned_data.get('price_max')
            obj = Product.objects.filter(category=categorys, brand__in=brands, bazar=bazars,
                                         price__gte=prices_min, price__lte=prices_max)
            return render(request, 'main/filter_list.html', context={'form': form, 'obj': obj})
    return render(request, 'category_list.html', context={'form': form})


class SearchView(generic.ListView):
    """Поиск по сайту"""
    model = Product
    template_name = 'search_res.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        return object_list



