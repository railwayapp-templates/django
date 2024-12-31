"""fhma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from client.views import add_client, ClientsViewSet, AreaServicedViewSet
from supplies.views import SuppliesViewSet, SupplyOrdersViewSet, SupplyOrderItemsViewSet
from survey.views import ClientSurvey2024ViewSet, ZipcodeSurveyViewSet, SurveyorViewSet, SurveyViewSet

router = DefaultRouter()
router.register(r'supplies', SuppliesViewSet, basename='supplies')
router.register(r'supply_orders', SupplyOrdersViewSet, basename='supply_orders')
router.register(r'supply_order_items', SupplyOrderItemsViewSet, basename='supply_order_items')
router.register(r'clients', ClientsViewSet, basename='clients')
router.register(r'clients_area_serviced', AreaServicedViewSet, basename='area_serviced')
router.register(r'clientsurveys2024', ClientSurvey2024ViewSet, basename='clientsurveys2024')
router.register(r'surveyors', SurveyorViewSet, basename='surveyors')
router.register(r'surveys', SurveyViewSet, basename='surveys')
router.register(r'zipcodesurveys', ZipcodeSurveyViewSet, basename='zipcodesurveys')

urlpatterns = [
    path('add-client/', add_client, name='add_client'),
    path('dashboards/', include('dashboards.urls', namespace='dashboards')),
    path('api/v1/', include(router.urls)),
    path('', admin.site.urls),
]
