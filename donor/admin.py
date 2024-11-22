from django.contrib import admin
from .models import Donor, Donation

from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Donor)
class DonorAdmin(ModelAdmin):
    list_display = ['name', 'email', 'phone', 'city', 'state', 'country', 'last_donated']
    search_fields = ['name', 'email', 'phone', 'city', 'state', 'country']
    list_filter = ['city', 'state', 'country', 'last_donated']

@admin.register(Donation)
class DonationAdmin(ModelAdmin):
    list_display = ['donor', 'amount', 'date']
    search_fields = ['donor__name', 'amount', 'date']
    list_filter = ['date']
    autocomplete_fields = ['donor']
