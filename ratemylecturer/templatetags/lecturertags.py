from django import template
from django.template.defaultfilters import slugify

register = template.Library()
@register.filter
def slug(value):
    return slugify(value)