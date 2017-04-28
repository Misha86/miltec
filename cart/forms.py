# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class SelectWidget(forms.Select):
    class Media:
        css = {
            'all': ('css/cart_select.css',)
        }


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='Количество', label_suffix='',
                                      widget=SelectWidget, choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    size = forms.TypedChoiceField(label='Размер', label_suffix='', choices=PRODUCT_QUANTITY_CHOICES,
                                  widget=SelectWidget)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

