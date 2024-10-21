from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Equipment, Order

@admin.register(Equipment)
class SaleAdmin(ModelAdmin):
    list_display = ["name", "stock", "barcode"]
    search_fields = ["name", "barcode"]
    list_filter = ["stock", "name"]

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["equipment", "quantity", "client", "status"]
    search_fields = ["equipment", "client"]
    list_filter = ["status", "client"]