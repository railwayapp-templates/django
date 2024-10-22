from django.contrib import admin
from .models import Supplies, SuppliesOrder

from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Supplies)
class SaleAdmin(ModelAdmin):
    list_display = ["name", "description", "quantity", "price"]
    search_fields = ["name", "description"]
    list_filter = ["name", "price", "quantity"]

@admin.register(SuppliesOrder)
class OrderAdmin(ModelAdmin):
    list_display = ["supplies", "quantity", "client", "delivery_date"]
    search_fields = ["supplies", "client"]
    list_filter = ["supplies", "client", "delivery_date"]
    autocomplete_fields = ["supplies", "client"]
    
