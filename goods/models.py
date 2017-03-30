# -*- encoding: utf-8 -*-
"""
This module create models for products.
"""

from __future__ import unicode_literals
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Stores a category for goods.
    """
    title = models.CharField(max_length=50, verbose_name="Назва категорії")
    used = models.BooleanField(verbose_name="Вживані", default=False)
    promotions = models.BooleanField(verbose_name="Знижені ціни", default=False)
    slug = models.SlugField(verbose_name="Ім`я категорії транслітом", unique=True)
    create = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    update = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        """
        Change db_table name, verbose_name, verbose_name_plural
        """
        db_table = "categories"
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)
