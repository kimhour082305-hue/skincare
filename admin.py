from django.contrib import admin
# pyrefly: ignore [missing-import]
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'discount_percentage')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'brand', 'code')
    list_editable = ('price', 'stock', 'discount_percentage')