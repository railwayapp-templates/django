from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin, TabularInline

from .models import Donor, Donation
from .forms import DonorForm

# Inline tabular view for donations in donor admin
class DonationInline(TabularInline):
    model = Donation
    fields = ['amount', 'date']
    readonly_fields = ['amount', 'date']
    ordering = ['date']
    max_num = 0
    show_change_link = True
    can_delete = False
    tab = True
    verbose_name = 'Donation'
    verbose_name_plural = 'Donations'

# Register donor model
@admin.register(Donor)
class DonorAdmin(ModelAdmin):
    form = DonorForm
    list_display = ['name', 'email', 'phone']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['name', 'email', 'phone']
    
    warn_unsaved_form = True  # Default: False
    list_disable_select_all = True 
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    inlines = [DonationInline]

# Register donation model
@admin.register(Donation)
class DonationAdmin(ModelAdmin):
    list_display = ['donor', 'amount', 'date']
    search_fields = ['donor__name', 'amount', 'date']
    list_filter = ['date']
    autocomplete_fields = ['donor']
    
    warn_unsaved_form = True  # Default: False
    list_disable_select_all = True 
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False
