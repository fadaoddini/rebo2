from django.contrib import admin
from django.contrib.admin import register


from info.models import Info, ServiceType, Service, Broker, Storage, Farmer


@register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'shaba', 'codemeli', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('mobile', 'shaba', 'codemeli')


@register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)


@register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)


@register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)


@register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'capacity', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)


@register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'number_tree', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)