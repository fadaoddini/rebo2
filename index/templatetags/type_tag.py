from django import template
from catalogue.models import Category, ProductType

register = template.Library()


@register.simple_tag
def get_type():
    return ProductType.objects.all()