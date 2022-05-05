from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import KorzinaAddProductForm
from .korzina import Korzina
from main.models import Product, TwiceProduct
from orders.forms import KuponForm


@require_POST
def korzina_add(request, product_id):
    korzina = Korzina(request)
    product = get_object_or_404(Product, id=product_id)
    form = KorzinaAddProductForm(request.POST)
    if form.is_valid():
        kz = form.cleaned_data
        if kz['quantity'] > product.stock:
            kz['quantity'] = product.stock
        korzina.add(product=product,
                 quantity=kz['quantity'],
                 update_quantity=kz['update'])
    return redirect('korzina:korzina_detail')

@require_POST
def korzina_tw_add(request, product_id):
    korzina = Korzina(request)
    product_tw = get_object_or_404(TwiceProduct, id=product_id)

    form = KorzinaAddProductForm(request.POST)
    if form.is_valid():
        kz = form.cleaned_data
        stock_list = [product.stock for product in product_tw.products.all()]
        if kz['quantity'] > min(stock_list):
            kz['quantity'] = min(stock_list)
        for product in product_tw.products.all():
            korzina.add(product=product,
                        quantity=kz['quantity'],
                        update_quantity=kz['update'])
    return redirect('korzina:korzina_detail')

def korzina_remove(request, product_id):
    korzina = Korzina(request)
    product = get_object_or_404(Product, id=product_id)
    korzina.remove(product)
    return redirect('korzina:korzina_detail')

def korzina_detail(request):
    korzina = Korzina(request)
    for item in korzina:
        item['update_quantity_form'] = KorzinaAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    kupon_form = KuponForm()
    return render(request,
                  'korzina/detail.html',
                  {'korzina': korzina,
                   'kupon_form': kupon_form})