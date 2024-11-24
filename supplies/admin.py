from django.contrib import admin
from client.models import Client
from .models import Supplies, SuppliesOrder

from unfold.admin import ModelAdmin

@admin.register(Supplies)
class SaleAdmin(ModelAdmin):
    list_display = ["name", "description", "quantity"]
    search_fields = ["name", "description"]
    list_filter = ["name", "quantity"]

@admin.register(SuppliesOrder)
class OrderAdmin(ModelAdmin):
    list_display = ["client", "delivery_date", "supplies", "quantity"]
    search_fields = ["supplies__name", "client__name"]  # Use related model fields
    list_filter = ["supplies", "client", "delivery_date"]
    autocomplete_fields = ["supplies", "client"]