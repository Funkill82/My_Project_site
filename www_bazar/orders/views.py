from django.shortcuts import render, redirect
from .models import OrderItem, Kupon, Order
from .forms import OrderCreateForm, KuponForm, OrderCreateOneClickForm
from korzina.korzina import Korzina
from django.utils import timezone
from django.views.decorators.http import require_POST
from main.models import User


def order_create(request):
    korzina = Korzina(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in korzina:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
                product = item['product']
                product.stock -= item['quantity']
                if not product.stock:
                    product.available = False
                product.save()
            korzina.clear() # очистка корзины
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'korzina': korzina, 'form': form})

def order_create_one_click(request):
    korzina = Korzina(request)

    if str(request.user) == 'AnonymousUser':
        if request.method == 'POST':
            form = OrderCreateOneClickForm(request.POST)
            if form.is_valid():
                tel = form.cleaned_data.get('tel')
                order = Order()
                order.save()
                for item in korzina:
                    OrderItem.objects.create(order=order, tel=tel, product=item['product'],
                                             price=item['price'], quantity=item['quantity'])
                    product = item['product']
                    product.stock -= item['quantity']
                    if not product.stock:
                        product.available = False
                    product.save()
                korzina.clear()  # очистка корзины
                return render(request, 'orders/order/created.html',
                              {'order': order})
        else:
            form = OrderCreateOneClickForm

        return render(request, 'orders/order/create1click.html',
                      {'korzina': korzina, 'form': form})
    else:

        user = User.objects.get(email=request.user)
        # print(request.user, user.tel)
        order = Order()
        order.save()
        for item in korzina:
            OrderItem.objects.create(order=order, tel= user.tel, product=item['product'],
                                     price=item['price'], quantity=item['quantity'])
            product = item['product']
            product.stock -= item['quantity']
            if not product.stock:
                product.available = False
            product.save()
        korzina.clear()  # очистка корзины
        return render(request, 'orders/order/create1click.html',
                      {'korzina': korzina})


@require_POST
def kupon_activate(request):
    now = timezone.now()
    form = KuponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            kupon = Kupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['kupon_id'] = kupon.id
        except Kupon.DoesNotExists:
            request.session['kupon_id'] = None
    return redirect('korzina:korzina_detail')