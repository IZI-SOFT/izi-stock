from django.contrib import admin
from .models import *


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['description', 'location', 'is_active', 'created_at', ]
    list_display_links = ['description']
    list_editable = ['is_active']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['description', 'branch', 'is_active', 'created_at']
    list_display_links = ['description']
    list_editable = ['is_active']


admin.site.site_title = "IZI STOCK"