from django.urls import path, re_path

from chat.views import index_chat, room_chat

urlpatterns = [
    path("", index_chat, name="index-chat"),
    path("<int:pk>/", room_chat, name="room"),
]
