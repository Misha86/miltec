from django.contrib import admin
from .models import (Product, Size, SizeCount)


class SizeCountInLine(admin.TabularInline):
    model = SizeCount


class ProductAdmin(admin.ModelAdmin):
    model = Product
    fieldsets = [
        (None, {'fields': ['title',  'description', 'details', 'article', 'sold',
                           'price', 'price_for_users', 'image', 'image_large', 'height_field', 'width_field', 'category', 'item']})
    ]
    list_display = ['title', 'category', 'item', 'id']
    readonly_fields = ['slug', 'update', 'height_field', 'width_field']
    inlines = [SizeCountInLine]


admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(SizeCount)
