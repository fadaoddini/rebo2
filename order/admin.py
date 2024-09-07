from django.contrib import admin
from django.contrib.admin import register

from order.models import Payment, Gateway, Order


@register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'faktor_number', 'amount', 'gateway', 'is_paid', 'product', 'authority')
    search_fields = ('user__username', 'product__name', 'faktor_number')
    list_editable = ('is_paid',)
    list_filter = ('gateway', 'is_paid')  # اضافه کردن فیلترها


@register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('title', 'gateway_code', 'is_enable')
    search_fields = ('title', 'gateway_code')
    list_filter = ('is_enable', 'gateway_code')


@register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'price', 'created_time', 'updated_time')
    search_fields = ('user__username',)
    list_filter = ('created_time', 'updated_time')
