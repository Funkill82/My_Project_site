from django import forms
from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('fio', 'email', 'delivery', 'bazar', 'payment', 'city')
        labels = {'fio': 'ФИО',  'delivery': 'Доставка',
                  'bazar': 'Магазин', 'payment': 'Способ оплаты', 'city': 'Город'}
class OrderCreateOneClickForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['tel']
        labels = {'tel': 'Номер телефона'}

class KuponForm(forms.Form):
    code = forms.CharField()

