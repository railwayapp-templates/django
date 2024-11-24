from django.contrib import admin
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from django.core.validators import EMPTY_VALUES

from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    MultipleRelatedDropdownFilter,
    RangeDateFilter,
    RangeNumericFilter,
    RelatedDropdownFilter,
    SingleNumericFilter,
    TextFilter,
)

from .models import Equipment, Order

@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ["name", "stock", "barcode"]
    search_fields = ["name", "barcode"]
    list_filter = ["stock", "name"]

class OrderStatuc(TextChoices):
    RENTED = "RT", _("Rented")
    RETURNED = "RU", _("Returned")

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["client", "show_status_customized_color", "equipment", "quantity"]
    list_filter = ["status", "client"]
    list_display_links = ["client", "show_status_customized_color", "equipment", "quantity"]
    search_fields = ["equipment", "client"]
    autocomplete_fields = ["equipment", "client"]
    
    @display(
        description=_("Status"),
        ordering="status",
        label=True
    )
    def show_status_default_color(self, obj):
        return obj.status

    @display(
        description=_("Status"),
        ordering="status",
        label={
            'Rented' : "danger",
            'Returned' : "success"
        },
    )
    def show_status_customized_color(self, obj):
        if obj.status == OrderStatuc.RENTED:
            return 'Rented'
        return 'Returned'

    