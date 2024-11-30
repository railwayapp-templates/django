from django.contrib import admin
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from django.core.validators import EMPTY_VALUES

from unfold.admin import ModelAdmin, TabularInline
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

from .models import Equipment, DMEOrder, DMEOrderItem
from .forms import DMEOrderItemFormSet, DMEOrderForm, DMEOrderItemForm

@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin):
    warn_unsaved_form = True  # Default: False
    list_disable_select_all = True 
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    list_display = ["name", "stock", "barcode"]
    search_fields = ["name", "barcode"]
    list_filter = ["stock", "name"]

class OrderItemInline(TabularInline):
    model = DMEOrderItem
    formset = DMEOrderItemFormSet
    extra = 0
    can_delete = True
    autocomplete_fields = ["equipment"]
    verbose_name = "Equipment Associated with Order"
    verbose_name_plural = "Equipment Associated with Order"


class OrderStatuc(TextChoices):
    RENTED = "RT", _("Rented")
    RETURNED = "RU", _("Returned")

@admin.register(DMEOrder)
class OrderAdmin(ModelAdmin):
    form = DMEOrderForm
    inlines = [OrderItemInline]
    warn_unsaved_form = True  # Default: False
    list_disable_select_all = True 
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    list_display = ["client", "show_status_customized_color"]
    list_filter = ["status", "client"]
    list_display_links = ["client", "show_status_customized_color"]
    search_fields = ["client"]
    autocomplete_fields = ["client"]
    verbose_name = "DME Order"
    verbose_name_plural = "DME Orders"
    
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

@admin.register(DMEOrderItem)
class DMEOrderItemAdmin(ModelAdmin):
    warn_unsaved_form = True
    list_display = ["equipment", "quantity"]
    autcomplete_fields = ["equipment"]
    search_fields = ["equipment"]

    