from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from .models import Product, UnderCategory

User = get_user_model()

class UserCreationForm(UserCreationForm):
    """Переопределение стандартных форм(не с админки) """
    email = forms.EmailField(max_length=254,label=_("Email"), widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    tel = forms.CharField(max_length=11, label='Телефон')
    captcha = CaptchaField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", 'tel')


class SortFilterForm(forms.ModelForm):
    """ Форма фильтра по продуктам """

    price_min = forms.DecimalField(max_digits=8, decimal_places=2, label='Минимальная цена')
    price_max = forms.DecimalField(max_digits=8, decimal_places=2, label='Максимальная цена')
    class Meta:
        model = Product
        fields = ['category', 'brand', 'price_min', 'price_max', 'bazar']
        labels = {'category': 'Категории', 'brand': 'Бренд',
                   'bazar': 'Магазин'}







