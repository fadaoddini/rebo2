from django.contrib import admin
from django.contrib.admin import register

from chat.models import Message, Chat


@register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'timestamp',)


@register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'room_name', )
