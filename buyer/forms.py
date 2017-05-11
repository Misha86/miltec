﻿# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django import forms
from .models import BuyerUser
from .admin import BuyerCreationForm


class CalendarWidget(forms.DateInput):
    class Media:
        css = {
            'all': ('css/jquery-ui.min.css',)
        }
        js = ('js/jquery-ui.js', 'js/datepicker-uk.js', 'js/datepicker-ru.js', 'js/datepicker-widget.js')


class RadioSelectWidget(forms.RadioSelect):
    class Media:
        css = {'all': ('css/radio_select.css', '//goo.gl/mTc43h')}


class BuyerLoginForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'E-Mail',
                                                                      'id': 'userid',
                                                                      'name': 'userid',
                                                                      'title': 'E-Mail'}))

    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': '•••••••••••',
                                                                           'id': 'pw',
                                                                           'name': 'pw',
                                                                           'title': 'password',
                                                                           'autocomplete': 'off'}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exists = BuyerUser.objects.filter(email=email).exists()
        if not email_exists:
            raise forms.ValidationError("Такой email не зареєстрован.", code='email_exists')
        else:
            return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        buyer = BuyerUser.objects.filter(email=email)
        if buyer.exists() and buyer[0].check_password(password):
            return password
        elif buyer.exists() and password is not None:
            raise forms.ValidationError("Неверный пароль!")


class BuyerRegisterForm(BuyerCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    sex = forms.ChoiceField(label="Пол", choices=(('Man', 'Мужчина'), ('Woman', 'Женщина')),
                            widget=RadioSelectWidget(attrs={'class': 'option-input radio'}))

    class Meta(BuyerCreationForm.Meta):
        model = BuyerUser

        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control', 'rows': 4,
                                                    'placeholder': 'введите E-mail'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control', 'rows': 4,
                                                        'placeholder': "введите имя"}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'rows': 4,
                                                       'placeholder': "введите фамилию"}),
                   'date_of_birth': CalendarWidget(format='%Y-%m-%d',
                                                   attrs={'class': 'form-control',
                                                          'id': 'id_date_of_birth',
                                                          'placeholder': 'дата рождения',
                                                          'autocomplete': 'off'}),
                   'phone_number': forms.TextInput(attrs={'class': 'form-control', 'rows': 4,
                                                          'placeholder': "введите номер телефона"}),
                   # 'sex': RadioSelectWidget(attrs={'class': 'option-input radio'})
}

        labels = {'email': "E-mail",
                  'first_name': "Имя",
                  'last_name': "Фамилия",
                  'date_of_birth': "Дата рождения",
                  # 'sex': "Пол",
                  'phone_number': "Номер телефона"}

        help_texts = {'phone_number': 'формат ввода номера телефона +380967578910'}


class BuyerUpdateForm(BuyerRegisterForm):
    password = forms.CharField(label="Старый пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'введите cтарый пароль',
                                                                 'autocomplete': 'off'}))
    email = forms.CharField(label="E-mail", disabled=True, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'rows': 4}))

    class Meta(BuyerRegisterForm.Meta):
        model = BuyerUser
        fields = BuyerRegisterForm.Meta.fields + ('address', 'password', )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        user = BuyerUser.objects.get(email=email)
        if user is not None and user.check_password(password):
            return password
        elif password is not None:
            raise forms.ValidationError("Старый пароль не верен!")