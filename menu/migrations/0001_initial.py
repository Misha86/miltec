# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-26 08:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Назва категорії')),
                ('used', models.BooleanField(default=False, verbose_name='Вживані')),
                ('promotions', models.BooleanField(default=False, verbose_name='Знижені ціни')),
                ('slug', models.SlugField(unique=True, verbose_name='Ім`я категорії транслітом')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
            ],
            options={
                'verbose_name_plural': 'Категорії',
                'verbose_name': 'Категорія',
                'db_table': 'categories',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Назва категорії')),
                ('used', models.BooleanField(default=False, verbose_name='Вживані')),
                ('promotions', models.BooleanField(default=False, verbose_name='Знижені ціни')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Ім`я категорії транслітом')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.Item')),
            ],
            options={
                'verbose_name_plural': 'Пункти категорій',
                'verbose_name': 'Пункти категорії',
                'db_table': 'items',
                'ordering': ['object_id', 'id'],
            },
        ),
    ]
