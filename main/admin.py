from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image_tag', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name', )}

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px" />',
                obj.image.url,
            )
        return format_html('<span>не має зображення</span>')
    
    image_tag.short_description = "Image"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}
