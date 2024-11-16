from django.urls import path
from .views import ClientDashboardView

app_name = 'client'

urlpatterns = [
    path('dashboard/', ClientDashboardView.as_view(), name='client_dashboard'),
]