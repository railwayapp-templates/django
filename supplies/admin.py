from django.contrib import admin
from django.db.models import Q

from client.models import Client
from .models import Supplies, SuppliesOrder, OrderItem
from .forms import SuppliesOrderForm, OrderItemFormSet

from unfold.admin import ModelAdmin, TabularInline


@admin.register(Supplies)
class SuppliesAdmin(ModelAdmin):
    warn_unsaved_form = True  # Default: False
    list_disable_select_all = True 
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    list_display = ["name", "description", "quantity"]
    search_fields = ["name", "description"]
    list_filter = ["name", "quantity"]


class OrderItemInline(TabularInline):
    model = OrderItem
    formset = OrderItemFormSet
    extra = 0
    can_delete = True
    autocomplete_fields = ["supplies"]
    verbose_name = "Order Item"
    verbose_name_plural = "Order Items"

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ["supplies", "quantity", "order"]
    search_fields = ["supplies__name", "order__client__name"]
    list_filter = ["supplies", "quantity", "order"]
    autocomplete_fields = ["supplies"]

@admin.register(SuppliesOrder)
class SuppliesOrderAdmin(ModelAdmin):
    form = SuppliesOrderForm
    inlines = [OrderItemInline]
    list_display = ["client", "delivery_date"]
    search_fields = ["client__name"]
    list_filter = ["client", "delivery_date"]
    autocomplete_fields = ["client"]