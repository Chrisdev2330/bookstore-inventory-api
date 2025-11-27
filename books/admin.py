from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    
    list_display = [
        'id',
        'title',
        'author',
        'isbn',
        'cost_usd',
        'selling_price_local',
        'stock_quantity',
        'category',
        'created_at',
    ]
    
    list_filter = [
        'category',
        'supplier_country',
        'created_at',
    ]
    
    search_fields = [
        'title',
        'author',
        'isbn',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    ordering = ['-created_at']
    
    list_per_page = 25
