import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Message, Chat
from chat.serializers import MessageSerializer
from rest_framework.renderers import JSONRenderer

from login.models import MyUser


class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        message = data['message']
        mobile = data['mobile']
        room_name = data['room_name']
        room_pk = data['room_pk']
        related_chat = Chat.objects.get(pk=room_pk)
        msg = Message.create(mobile, message, related_chat)
        # msg_content = str(msg.content)
        msg_content = eval(self.message_serializer(msg))

        self.send_to_chat_message(msg_content)

    def fetch_message(self, data):

        message = data.get("message", None)
        mobile = data.get("mobile", None)
        room_name = data.get("room_name", None)
        room_pk = data.get("room_pk", None)
        query = Message.last_message(self, room_pk)
        message_json = self.message_serializer(query)
        content = {
            "message": eval(message_json),
            "command": "fetch_message",
            "room_pk": room_pk,
            "room_name": room_name
        }
        self.chat_message(content)

    def message_serializer(self, query):
        if query.__class__.__name__ == 'QuerySet':
            status_boolean = True
        else:
            status_boolean = False
        serialized_msg = MessageSerializer(query, many=status_boolean)
        content = JSONRenderer().render(serialized_msg.data)
        return content

    # start connection from client to server
    def connect(self):
        self.set_user_mode_online(self.scope['user'].pk)
        self.room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        self.room_group_name = f"chat_{self.room_pk}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    commands = {
        "new_message": new_message,
        "fetch_message": fetch_message
    }

    # finished connection from client to server
    def disconnect(self, close_code):

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.set_user_mode_offline(self.scope['user'].pk)

    # Receive message from WebSocket from client and GET data
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        command = text_data_json["command"]
        room_name = text_data_json["room_name"]
        room_pk = text_data_json["room_pk"]
        self.commands[command](self, text_data_json)

        # Send new message to room group
        # GET data AS new_message in LINE : 14
    def send_to_chat_message(self, message):

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "content": message['content'],
                "command": "new_message",
                "__str__": message['__str__'],
                "time_persian": message['time_persian']
             }
        )

    # Receive message from room group
    # GET data AS fetch_message in LINE : 26
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))

    def set_user_mode_offline(self, pk):
        MyUser.set_offline(pk)
        information = MyUser.get_user_info(pk)

    def set_user_mode_online(self, pk):
        MyUser.set_online(pk)
        information = MyUser.get_user_info(pk)

