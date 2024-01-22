import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from login.myusermanager import MyUserManager


class MyUser(AbstractUser):
    ONLINE = True
    OFFLINE = False

    ONLINE_OFFLINE = (
        (ONLINE, "online"),
        (OFFLINE, "offline")
    )

    username = None
    mobile = models.CharField(max_length=11, unique=True)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)
    last_time_online = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='image_profile/' + str(uuid.uuid4()) + "/", null=True,
                              blank=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
    backend = 'login.mybackend.MobileBackend'

    @classmethod
    def set_online(cls, pk):
        user = MyUser.objects.filter(pk=pk).first()
        user.user_mode = True
        user.save()

    @classmethod
    def set_offline(cls, pk):
        user = MyUser.objects.filter(pk=pk).first()
        user.user_mode = False
        user.save()

    @classmethod
    def get_user_info(self, pk):
        user = MyUser.objects.filter(pk=pk).first()
        res = user.first_name+" "+user.last_name
        return res
