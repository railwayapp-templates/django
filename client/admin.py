from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin, TabularInline

from .models import Client, AreaServiced
from supplies.models import SuppliesOrder
from equipment.models import Order

class SuppliesInline(TabularInline):
    model = SuppliesOrder
    fields = ["supplies", "quantity", "delivery_date"]
    readonly_fields = ["supplies", "quantity", "delivery_date"]
    ordering_field = "delivery_date"
    max_num = 0
    show_change_link = True
    tab = True
    verbose_name = "Inconnient Supplies Order"
    verbose_name_plural = "Inconnient Supplies Orders"

class EquipmentInline(TabularInline):
    model = Order
    fields = ["equipment", "status", "quantity"]
    readonly_fields = ["equipment", "quantity"]
    ordering_field = "status"
    max_num = 0
    show_change_link = True
    tab = True
    verbose_name = "Durable Medical Equipment Order"
    verbose_name_plural = "Durable Medical Equipment Orders"

@admin.register(AreaServiced)
class AreaServicedAdmin(ModelAdmin):
    warn_unsaved_form = True  # Default: False

    list_display = ["name", "zipcode"]
    search_fields = ["name", "zipcode"]
    list_filter = ["name", "zipcode"]

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    warn_unsaved_form = True  # Default: False
    list_disable_select_all = True 
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    list_display = ["name", "area_serviced", "is_active"]
    search_fields = ["name", "email", "phone", "address", "city", "state", "country", "area_serviced__name", "is_active"]
    list_filter = ["name", "email", "phone", "address", "city", "state", "area_serviced", "country", "is_active"]
    list_display_links = ["name", "area_serviced", "is_active"]
    autocomplete_fields = ["area_serviced"]

    inlines = [SuppliesInline, EquipmentInline]

    fieldsets = (
        (
            _("Client Details"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
                    "age",
                    "is_active",
                    "email",
                    "phone",
                    "address",
                    "city",
                    "state",
                    "country",
                    "zipcode",
                ],
            },
        ),
        (
            _("Demographic Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "ethnicity",
                    "below_poverty_line",
                    "homeless",
                    "veteran",
                    "disabled",
                ],
            },
        ),
    )
