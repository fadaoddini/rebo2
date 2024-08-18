from django.contrib import admin
from django.contrib.admin import register
import math
from transport.models import Transport, TransportType, TransportReq, Location, RouteMetrics, PriceList


@register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('min_cost_per_one_ton', 'max_cost_per_one_ton', 'min_cost_per_one_km', 'max_cost_per_one_km',  )


@register(TransportType)
class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)


@register(Transport)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'transport_type', 'pelak', 'capacity', 'user', 'status')
    list_filter = ('pelak', 'status')
    list_editable = ('status', )
    search_fields = ('car_name', 'user', 'pelak')
    actions = ('active_all', 'deactive_all')

    def active_all(self, request, queryset):
        for queryone in queryset:
            transport = Transport.objects.filter(pk=queryone.pk).first()
            transport.status = True
            transport.save()

    def deactive_all(self, request, queryset):
            for queryone in queryset:
                transport = Transport.objects.filter(pk=queryone.pk).first()
                transport.status = False
                transport.save()


@register(TransportReq)
class TransportReqAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'distance', 'price', 'barnameh', 'my_transport', 'status')
    list_filter = ('origin', 'destination')
    list_editable = ('status', )
    search_fields = ('origin', 'destination', 'my_transport')
    actions = ('active_all', 'deactive_all')

    def active_all(self, request, queryset):
        for queryone in queryset:
            transportReq = TransportReq.objects.filter(pk=queryone.pk).first()
            transportReq.status = True
            transportReq.save()

    def deactive_all(self, request, queryset):
            for queryone in queryset:
                transportReq = TransportReq.objects.filter(pk=queryone.pk).first()
                transportReq.status = False
                transportReq.save()


@register(RouteMetrics)
class RouteMetricsAdmin(admin.ModelAdmin):
    list_display = (
        'origin', 'destination', 'distance_km', 'min_duration_hours', 'max_duration_hours', 'min_cost', 'max_cost', 'transport_capacity'
    )
    list_filter = ('origin', 'destination')
    search_fields = ('origin__name', 'destination__name')

    def save_model(self, request, obj, form, change):
        # Save the model to trigger the save method which performs calculations
        if obj.origin and obj.destination:
            obj.save()
        else:
            # If origin or destination is missing, just save the model without calculations
            super().save_model(request, obj, form, change)


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)
    list_filter = ('name',)