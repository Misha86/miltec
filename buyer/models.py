# -*- encoding: utf-8 -*-
"""
This module create custom buyer-user.
"""

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
# from django_phonenumbers.model.fields import PhoneNumberField
from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField


class MyUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, date_of_birth, sex, address, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Профиль должен иметь электронный адрес')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            address=address,
            phone_number=phone_number,
            sex=sex
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name,  last_name,
                         address, phone_number, sex):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
            sex=sex
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BuyerUser(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Электронный адрес',
        max_length=255,
        unique=True,
        )

    first_name = models.CharField('Имя', max_length=25)
    last_name = models.CharField('Фамилия', max_length=25)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    sex = models.CharField(max_length=20, choices=(('Man', 'Мужчина'), ('Woman', 'Женщина')),
                           verbose_name="Стать")

    address = AddressField(verbose_name="Адрес", max_length=500)
    phone_number = PhoneNumberField(verbose_name='Телефонный номер')

    profile_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания профиля")
    profile_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления профиля")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'sex', 'address', 'phone_number']

    class Meta:
        verbose_name = "профиль покупателя"
        verbose_name_plural = "профиля покупателей"

    def get_full_name(self):
        # The user is identified by their email address
        return '{} {}'.format(self.last_name, self.first_name)
    get_full_name.admin_order_field = 'profile_create'
    get_full_name.short_description = 'Фамилия и имя'

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        # __unicode__ on Python 2
        return self.email

    def get_sex(self):
        return self.get_sex_display()
    get_sex.admin_order_field = 'sex'
    get_sex.short_description = 'Стать покупателя'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
