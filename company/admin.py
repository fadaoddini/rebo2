from django.contrib import admin
from django.contrib.admin import register

from company.models import Warehouse, CustomerBalance, TransferWarehouse, \
    Company, Location, Customer, Driver, Staff, TypeDates


@register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('company', 'driver', 'customer', 'typedate', 'quantity', 'transfer_type', 'value_type',
                    'created_time')
    list_filter = ('transfer_type', 'value_type', 'typedate')
    search_fields = ('company', 'driver', 'customer', 'quantity', 'typedate')


@register(CustomerBalance)
class CustomerBalanceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'typedate', 'balance', 'created_time')
    search_fields = ('customer__family',)


@register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_active', 'created_time')
    search_fields = ('user__name', 'name')


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'address')
    search_fields = ('company__name', 'name', 'address')


@register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'family', 'mobile', 'country', 'city')
    search_fields = ('company__name', 'name', 'family', 'mobile', 'country', 'city')


@register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'family', 'mobile', 'plaque', 'vasat', 'iran')
    search_fields = ('company__name', 'name', 'family', 'mobile', 'plaque', 'vasat', 'iran')


@register(TypeDates)
class TypeDatesAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'type')
    search_fields = ('company__name', 'name', 'type')


@register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('location', 'name', 'family', 'mobile', 'card_number', 'role', 'insurance',
                    'insurance_status', 'fix_salary', 'salon', 'status')
    search_fields = ('location__name', 'name', 'family', 'mobile', 'card_number')
    list_filter = ('location__name', 'role', 'insurance', 'salon', 'status', )


@register(TransferWarehouse)
class TransferWarehouseAdmin(admin.ModelAdmin):
    list_display = ('sender_transfer', 'received_transfer',
                    'typedate', 'quantity', 'created_time')
    search_fields = ('sender_transfer', 'received_transfer',
                     'typedate', 'quantity', 'created_time')




