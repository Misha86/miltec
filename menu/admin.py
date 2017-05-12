from django.contrib import admin
from django.contrib.contenttypes.admin import (GenericStackedInline, GenericTabularInline)
from .models import (Category, Item)
from product.models import (Product, Size)


class SizeInLine(admin.TabularInline):
    model = Size.items.through
    extra = 2


class ProductInLine(admin.StackedInline):
    model = Product
    fieldsets = [
        # (None, {
        #     'fields': [('title', 'article', 'slug'), ('description', 'details'), ('image', 'image_large'),
        #                ('sold', 'price', 'price_for_users'), ('category', 'item')]}),
        ('Скриті дані', {
            'classes': ('collapse',),
            'fields': (('title', 'article', 'slug'), ('description', 'details'), ('image', 'image_large'),
                       ('sold', 'price', 'price_for_users'), ('category', 'item')),
        }),
    ]
    extra = 0
    verbose_name = 'Товар категорії'
    verbose_name_plural = "Товари категорії"
    readonly_fields = ['slug', 'sold', 'category', 'item']


class ItemInLine(GenericStackedInline):
    model = Item
    fieldsets = [
        # (None, {'fields': ['title', 'used', 'promotions', 'slug']}),
        ('Скриті дані', {
            'classes': ('collapse',),
            'fields': ('title', 'used', 'promotions', 'slug'),
        }),
    ]
    extra = 1
    verbose_name = 'Пункт категорії'
    verbose_name_plural = "Пункти категорії"
    readonly_fields = ['slug', ]


class ItemsInLine(GenericTabularInline):
    model = Item
    extra = 2
    verbose_name = 'Підпункт'
    verbose_name_plural = "Підпункти"
    readonly_fields = ['slug']

    # radio_fields = {'parent': admin.VERTICAL, }


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    fieldsets = [
        (None, {'fields': ['title',  'used', 'promotions', 'slug', 'image', 'create', 'update']})
    ]
    list_display = ['title', 'create', 'slug', 'used', 'promotions', 'id']
    readonly_fields = ['slug', 'create', 'update']
    inlines = [ItemInLine]


class ItemAdmin(admin.ModelAdmin):
    model = Item
    fieldsets = [
        (None, {'fields': ['title', 'used', 'promotions', 'parent', 'content_type', 'object_id', 'slug', 'create', 'update', 'pk']})
    ]
    list_display = ['title', 'used', 'promotions', 'content_object',  'parent', 'id']
    readonly_fields = ['slug', 'create', 'update', 'pk']
    list_select_related = ('parent', )

    search_fields = ['title', ]
    list_per_page = 10

    inlines = [ItemsInLine, SizeInLine, ProductInLine]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)