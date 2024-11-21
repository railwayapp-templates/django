from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Survey, Surveyor, ClientSurvey2024

@admin.register(Survey)
class SaleAdmin(ModelAdmin):
    list_display = ["meet_expectations", "volunteer_helpful", "comments", "service_impact", "refer_friends"]
    search_fields = ["meet_expectations", "volunteer_helpful", "comments", "service_impact", "refer_friends"]
    list_filter = ["meet_expectations", "volunteer_helpful", "comments", "service_impact", "refer_friends"]

@admin.register(Surveyor)
class SurveyorAdmin(ModelAdmin):
    list_display = ["name", "email", "phone", "organization"]
    search_fields = ["name", "email", "phone", "organization"]
    list_filter = ["name", "email", "phone", "organization"]

@admin.register(ClientSurvey2024)
class ClientSurvey2024Admin(ModelAdmin):
    list_display = ["uti_lastyear"]
    search_fields = ["uti_lastyear"]
    list_filter = ["uti_lastyear"]