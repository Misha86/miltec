# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-04 06:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0002_auto_20170404_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Назва категорії')),
                ('description', models.TextField(max_length=5000, verbose_name='Опис товару')),
                ('article', models.PositiveIntegerField(default=0, verbose_name='Артикль товару')),
                ('sold', models.BooleanField(default=False, verbose_name='Проданий')),
                ('slug', models.SlugField(unique=True, verbose_name='Ім`я товару транслітом')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Ціна для всій відвідувачів')),
                ('price_for_users', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна для зареєстрованих відвідувачів')),
                ('image', models.ImageField(blank=True, height_field='height_field', help_text='Зображення товару', null=True, upload_to=product.models.upload_location, verbose_name='Картинки', width_field='width_field')),
                ('width_field', models.IntegerField(default=0, verbose_name='Ширина картинки в пікселях')),
                ('height_field', models.IntegerField(default=0, verbose_name='Висота картинки в пікселях')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='menu.Category', verbose_name='Категорія товару')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='menu.Item', verbose_name='Підкатегорія товару')),
            ],
            options={
                'verbose_name': 'Товар',
                'ordering': ['id'],
                'verbose_name_plural': 'Товари',
                'db_table': 'products',
            },
        ),
    ]