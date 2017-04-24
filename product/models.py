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


def upload_location(instance, filename):
    path = 'upload/products'
    if instance.category:
        dir = instance.category.title
    else:
        dir = instance.item.title
    return os.path.join(path, str(dir), str(instance.title), 'detail', str(filename))


def upload_location2(instance, filename):
    path = 'upload/products'
    if instance.category:
        dir = instance.category.title
    else:
        dir = instance.item.title
    return os.path.join(path, str(dir), str(instance.title), str(filename))


class Product(models.Model):
    """
    Stores a product.
    """
    title = models.CharField(max_length=50, verbose_name="Назва категорії")
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

        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:product', kwargs={
            'slug': self.slug})
