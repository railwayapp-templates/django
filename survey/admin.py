from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Survey

@admin.register(Survey)
class SaleAdmin(ModelAdmin):
    list_display = ["meet_expectations", "volunteer_helpful", "comments", "service_impact", "refer_friends"]
    search_fields = ["meet_expectations", "volunteer_helpful", "comments", "service_impact", "refer_friends"]
    list_filter = ["meet_expectations", "volunteer_helpful", "comments", "service_impact", "refer_friends"]