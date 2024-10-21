from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Equipment

@admin.register(Equipment)
class SaleAdmin(ModelAdmin):
    list_display = ["name", "stock", "barcode"]
    search_fields = ["name", "barcode"]
    list_filter = ["stock", "name"]