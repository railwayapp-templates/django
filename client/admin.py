from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from unfold.admin import ModelAdmin
from unfold.views import UnfoldModelAdminViewMixin

from .models import Client, AreaServiced

@admin.register(AreaServiced)
class AreaServicedAdmin(ModelAdmin):
    list_display = ["name", "zipcode"]
    search_fields = ["name", "zipcode"]
    list_filter = ["name", "zipcode"]

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["name", "area_serviced"]
    search_fields = ["name", "email", "phone", "address", "city", "state", "area_serviced", "country"]
    list_filter = ["name", "email", "phone", "address", "city", "state", "area_serviced", "country"]
    autocomplete_fields = ["area_serviced"]