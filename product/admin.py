from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    model = Product
    fieldsets = [
        (None, {'fields': ['title',  'description', 'article', 'sold',
                           'price', 'price_for_users', 'image', 'image_large', 'height_field', 'width_field', 'category', 'item']})
    ]
    list_display = ['title', 'category', 'item', 'id']
    readonly_fields = ['slug', 'update', 'height_field', 'width_field']


admin.site.register(Product, ProductAdmin)
