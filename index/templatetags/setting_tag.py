from django import template
from index.models import SettingApp

register = template.Library()


@register.simple_tag
def get_setting():
    return SettingApp.objects.first()
