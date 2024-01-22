from django.contrib import admin
from django.contrib.admin import register

from bid.models import Bid


@register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('price', 'user', 'product_id', 'result')
