from django.contrib import admin
from django.contrib.contenttypes.admin import (GenericStackedInline, GenericTabularInline)
from .models import (Category, Item)
from product.models import Product


class ProductInLine(admin.StackedInline):
    model = Product
    fieldsets = [
        (None, {
            'fields': ['title', 'description', 'image', 'image_large', 'article', 'sold', 'slug']}),
        ('Ціна', {
            'fields': ['price', 'price_for_users']}),
        ('Категорії', {
            'fields': ['category', 'item']})
    ]
    extra = 1
    verbose_name = 'Товар категорії'
    verbose_name_plural = "Товари категорії"
    readonly_fields = ['slug', 'sold']


class ItemInLine(GenericStackedInline):
    model = Item
    fieldsets = [
        (None, {'fields': ['title', 'used', 'promotions', 'slug']})
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
        (None, {'fields': ['title',  'used', 'promotions', 'slug', 'create', 'update']})
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

    inlines = [ItemsInLine, ProductInLine]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)