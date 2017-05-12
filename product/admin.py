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


class SizeAdmin(admin.ModelAdmin):
    model = Size
    list_display = ['title', 'get_items', 'id']
    search_fields = ['title', 'items', ]
    list_filter = ['items', ]


class SizeCountAdmin(admin.ModelAdmin):
    model = SizeCount
    list_display = ['size', 'product', 'count', 'id']
    search_fields = ['product', 'size', ]
    list_filter = ['size', ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(SizeCount, SizeCountAdmin)
