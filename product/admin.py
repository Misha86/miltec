from django.contrib import admin
from .models import (Product, Size, SizeCount)


class SizeCountInLine(admin.TabularInline):
    model = SizeCount
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    model = Product
    date_hierarchy = 'create'
    fieldsets = [
        (None, {'fields': [('title', 'article', 'slug'), ('description', 'details'),
                           ('sold', 'price', 'price_for_users'), ('image', 'image_large'),
                           ('height_field', 'width_field'), ('category', 'item')]})
    ]
    list_display = ['title', 'article', 'category', 'item', 'id']
    readonly_fields = ['slug', 'update', 'height_field', 'width_field']
    search_fields = ['title', 'article', ]
    # list_editable = ('article', 'category', 'item')
    list_filter = ['category', 'item']
    list_select_related = ('category', 'item')
    inlines = [SizeCountInLine]


admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(SizeCount)
