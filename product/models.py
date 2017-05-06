# -*- encoding: utf-8 -*-
"""
This module create models for products.
"""

from __future__ import unicode_literals

import os
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from menu.models import (Category, Item)
from cart.forms import CartAddProductForm


def upload_location(instance, filename):
    path = 'upload/products'
    if instance.category:
        dir = instance.category.title
    else:
        dir = instance.item.title
    return os.path.join(path, str(dir), str(instance.article), 'detail', str(filename))


def upload_location2(instance, filename):
    path = 'upload/products'
    if instance.category:
        dir = instance.category.title
    else:
        dir = instance.item.title
    return os.path.join(path, str(dir), str(instance.article), str(filename))


class Product(models.Model):
    """
    Stores a product.
    """
    title = models.CharField(max_length=50, verbose_name="Назва товару")
    description = models.TextField(max_length=5000, verbose_name="Опис товару")
    details = models.TextField(max_length=5000, verbose_name="Деталі товару", default='')
    article = models.PositiveIntegerField(verbose_name="Артикль товару", default=00000000)

    sold = models.BooleanField(verbose_name="Проданий", default=False)
    slug = models.SlugField(verbose_name="Ім`я товару транслітом", unique=True)

    price = models.DecimalField(verbose_name="Ціна для всій відвідувачів",
                                max_digits=8, decimal_places=2)
    price_for_users = models.DecimalField(verbose_name="Ціна для зареєстрованих відвідувачів",
                                          max_digits=10, decimal_places=2)

    image = models.ImageField(verbose_name="Картинка", upload_to=upload_location, width_field="width_field",
                              height_field="height_field", blank=True, null=True,
                              help_text="Зображення товару")
    image_large = models.ImageField(verbose_name="Велика картинка", upload_to=upload_location2, width_field="width_field",
                                    height_field="height_field", blank=True, null=True,
                                    help_text="Зображення товару для детального перегляду")
    width_field = models.IntegerField(default=0, verbose_name="Ширина картинки в пікселях")
    height_field = models.IntegerField(default=0, verbose_name="Висота картинки в пікселях")

    create = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    update = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    category = models.ForeignKey(Category, related_name="products",
                                 verbose_name="Категорія товару", blank=True, null=True)

    item = models.ForeignKey(Item, related_name="products",
                             verbose_name="Підкатегорія товару", blank=True, null=True)

    class Meta:
        """
        Change db_table name, verbose_name, verbose_name_plural
        """
        ordering = ['id']
        db_table = "products"
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.category:
            object_id = self.category.id
        elif self.item:
            object_id = self.item.id
        else:
            object_id = self.article
        self.slug = "{}-{}".format(slugify(self.title, allow_unicode=True), object_id)

        if not self.category:
            self.category = self.item.category()

        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:product', kwargs={
            'slug': self.slug})

    def get_sizes(self):
        instance_sizes = Size.objects.filter(size_count__product=self)
        if not instance_sizes.exists():
            return None
        else:
            return instance_sizes

    def get_cart_form(self, request_form=None):
        if request_form is None:
            cart_form = CartAddProductForm()
        else:
            cart_form = CartAddProductForm(request_form)
        sizes = self.get_sizes()
        cart_form.fields['quantity'].choices = [(i, str(i)) for i in range(1, 21)]
        if sizes:
            size_choices = [(sizes[i], str(sizes[i])) for i in range(len(sizes))]
            cart_form.fields['size'].choices = size_choices
        else:
            cart_form.fields['size'].choices = []
        return cart_form

    def get_item_products(self):
        all_products = self.item.products.all()
        return all_products


class Size(models.Model):
    title = models.CharField(verbose_name="Размер", max_length=10)
    items = models.ManyToManyField(Item, related_name="sizes",
                                   verbose_name="Категория размера")

    class Meta:
        """
        Size products for item
        """
        ordering = ['title']
        db_table = "sizes"
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return self.title


class SizeCount(models.Model):
    size = models.ForeignKey(Size, related_name='size_count')
    product = models.ForeignKey(Product, related_name='size_count')
    count = models.IntegerField(verbose_name="Количество", default=0)

    class Meta:
        """
        Count sizes of products for item
        """
        verbose_name = "Количество размеров"
        verbose_name_plural = "Количества размеров"

    def __str__(self):
        return "Количество размера - {}: {}".format(self.size.title, self.count)