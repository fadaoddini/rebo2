from django.contrib import admin
from django.contrib.admin import register

from index.models import SettingApp


@register(SettingApp)
class SettingAppAdmin(admin.ModelAdmin):
    list_display = ('title', 'tel', 'mobile', 'email', 'is_active')
    list_editable = ('is_active',)
