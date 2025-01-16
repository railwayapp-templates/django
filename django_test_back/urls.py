from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # ...existing code...
    path('ola/', views.hello_page, name='hello'),
    # ...existing code...
]
