from django.db import models
from django.contrib.auth import get_user_model

from login.models import MyUser

user = get_user_model()


class Chat(models.Model):
    room_name = models.CharField(max_length=55, blank=True, null=True, unique=True)
    members = models.ManyToManyField(user, blank=True)

    def __str__(self):
        return self.room_name

    # get all members in chatroom by pk
    @classmethod
    def get_members(cls, pk):
        result = Chat.objects.filter(pk=pk).first()
        members = result.members.all()
        return members

    @classmethod
    def get_room_name(cls, pk):
        result = Chat.objects.filter(pk=pk).first()
        room_name = result.room_name
        return room_name

    @property
    def count_member(self):
        return self.members.count()


class Message(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    related_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chats',
                                 blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def last_message(self, room_pk):
        return Message.objects.filter(related_chat__pk=room_pk).order_by('-timestamp')

    @classmethod
    def create(cls, mobile, message, related_chat, *args, **kwargs):
        context = dict()
        author = MyUser.objects.filter(mobile=mobile).first()
        new_message = Message(author=author, content=message, related_chat=related_chat)
        new_message.save()
        return new_message

    def __str__(self):
        return self.author.mobile

