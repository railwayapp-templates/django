from django.contrib import admin
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from django.core.validators import EMPTY_VALUES
from django.contrib.auth.models import AbstractUser

from unfold.admin import ModelAdmin

from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(AbstractUser)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ["username", "email", "is_staff", "is_active"]
    search_fields = ["username", "email"]
    list_filter = ["is_staff", "is_active"]