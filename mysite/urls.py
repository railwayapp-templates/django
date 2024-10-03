"""
URL configuration for demosite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from .views import home_view, login_view, register_view, logout_view, api_data_view, api_data_view_2, api_data_view_4

urlpatterns = [
    path('', home_view, name="home"),
    path('login/', login_view, name="login"),
    path('register/', register_view),
    path('logout/', logout_view, name="logout"),
    path('api-data/', api_data_view, name='api-data'),
    path('api-data2/', api_data_view_2, name='api-data2'),
    path('api-data4/', api_data_view_4, name='api-data4'),
    path('admin/', admin.site.urls),
]
