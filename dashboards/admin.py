from django.urls import path
from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import ClientDashboard
from .views import ClientDashboardView


@admin.register(ClientDashboard)
class CustomAdmin(ModelAdmin):
    def get_urls(self):
        return super().get_urls() + [
            path(
                "dashboards/client",
                ClientDashboardView.as_view(model_admin=self),  # IMPORTANT: model_admin is required
                name="client_dashboard"
            ),
        ]