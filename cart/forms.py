# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django import forms


class SelectWidget(forms.Select):
    class Media:
        css = {
            'all': ('css/cart_select.css',)
        }


class CartAddProductForm(forms.Form):

    quantity = forms.TypedChoiceField(label='Количество', label_suffix='',
                                      widget=SelectWidget, coerce=int)
    size = forms.TypedChoiceField(label='Размер', label_suffix='', required=False,
                                  widget=SelectWidget)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
