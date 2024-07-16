from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'price', 'available', 'created_at', 'updated_at')
    list_filter = ('category', 'available', 'created_at', 'updated_at')
    ordering = ('title',)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',)
        }
