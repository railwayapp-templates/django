from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Client, AreaServiced

@admin.register(AreaServiced)
class AreaServicedAdmin(ModelAdmin):
    list_display = ["name", "zipcode"]
    search_fields = ["name", "zipcode"]
    list_filter = ["name", "zipcode"]

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["name", "email", "phone", "address", "city", "state", "area_serviced", "country"]
    search_fields = ["name", "email", "phone", "address", "city", "state", "area_serviced", "country"]
    list_filter = ["name", "email", "phone", "address", "city", "state", "area_serviced", "country"]
    autocomplete_fields = ["area_serviced"]