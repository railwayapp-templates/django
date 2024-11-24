from django.contrib import admin
from django.db.models import Q

from client.models import Client
from .models import Supplies, SuppliesOrder

from unfold.admin import ModelAdmin


@admin.register(Supplies)
class SuppliesAdmin(ModelAdmin):
    warn_unsaved_form = True  # Default: False
    list_disable_select_all = True 
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    list_display = ["name", "description", "quantity"]
    search_fields = ["name", "description"]
    list_filter = ["name", "quantity"]


@admin.register(SuppliesOrder)
class OrderAdmin(ModelAdmin):
    warn_unsaved_form = True  # Default: False
    list_disable_select_all = True 
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    list_display = ["client", "delivery_date", "supplies", "quantity"]
    list_display_links = ["client", "delivery_date", "supplies", "quantity"]
    search_fields = ["supplies__name", "client__name", "client"]  # Use related model fields
    list_filter = ["supplies", "client", "delivery_date"]
    autocomplete_fields = ["supplies", "client"]