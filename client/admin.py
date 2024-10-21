from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Client

@admin.register(Client)
class SaleAdmin(ModelAdmin):
    list_display = ["name", "email", "phone", "address", "city", "state", "zip", "country"]
    search_fields = ["name", "email", "phone", "address", "city", "state", "zip", "country"]
    list_filter = ["name", "email", "phone", "address", "city", "state", "zip", "country"]
    