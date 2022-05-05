from itertools import count

from django import forms



class KorzinaAddProductForm(forms.Form):
    PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Колличество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)







