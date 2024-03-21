# user_tags.py
from django import template

register = template.Library()

@register.filter(name='user_type')
def user_type(user):
    return type(user).__name__
