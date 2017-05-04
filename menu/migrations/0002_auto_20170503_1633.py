# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-03 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import menu.models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='height_field',
            field=models.IntegerField(default=0, verbose_name='Висота картинки в пікселях'),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', help_text='Картинка категории', null=True, upload_to=menu.models.upload_location, verbose_name='Картинка', width_field='width_field'),
        ),
        migrations.AddField(
            model_name='category',
            name='width_field',
            field=models.IntegerField(default=0, verbose_name='Ширина картинки в пікселях'),
        ),
    ]
