from django.contrib import admin
from django.contrib.admin import register

from transaction.models import Transaction, UserBalance, TransferTransaction, UserScore


@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'created_time')
    list_filter = ('transaction_type',)
    search_fields = ('user', 'transaction_type', 'amount', 'created_time')


@register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_time')
    search_fields = ('user__name',)


@register(TransferTransaction)
class TransferTransactionAdmin(admin.ModelAdmin):
    list_display = ('sender_transaction', 'sender_name', 'received_transaction',
                    'received_name', 'amount', 'created_time')
    search_fields = ('sender_transaction', 'sender_name', 'received_transaction',
                     'received_name', 'amount', 'created_time')


@register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score')
    search_fields = ('user',)




