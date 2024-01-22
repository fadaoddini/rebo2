from django.conf import settings
from django.shortcuts import redirect
from suds.client import Client
from info.models import Info


def check_is_active(user):
    return user.is_active


def check_is_ok(user, pk):
    if user.pk == pk:
        return True
    return False


def check_user_active(user):
    check_info = Info.objects.filter(user=user).first()
    if check_info is None:
        return False
    if user.info.is_active is True:
        return True
    return False

