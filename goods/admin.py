from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['title', 'create', 'slug', 'used', 'promotions']
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)
