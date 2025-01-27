from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'created_at', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'category','price', 'quantity','manufacture_date', 'expiration_date', 'created_at']


