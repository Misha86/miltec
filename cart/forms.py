# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django import forms
from buyer.forms import BuyerRegisterForm


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


class SendMassageForm(BuyerRegisterForm):

    address = forms.CharField(label='Адрес новой почти',
                              widget=forms.TextInput(attrs={'placeholder': 'выбирите адрес отделения новой почты'}),
                              help_text='Відділення №7 вулиця Корольова, 15А, Рівне, Рівненська область')

    cart_email = forms.EmailField(label='E-mail',
                                  required=False, widget=forms.EmailInput(attrs={'placeholder': 'E-Mail',
                                                                                 'id': 'userid',
                                                                                 'name': 'userid',
                                                                                 'title': 'E-Mail'}))
    password1 = None
    password2 = None
    sex = None

    class Meta(BuyerRegisterForm.Meta):
        exclude = ['date_of_birth', 'sex', 'password', 'email']
