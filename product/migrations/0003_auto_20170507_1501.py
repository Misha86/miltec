# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-07 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20170507_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Опис товару'),
        ),
    ]
