# core/templatetags/split_filter.py
from django import template

register = template.Library()

@register.filter
def split(value, sep):
    """
    Splits the string by sep. 
    Usage: {{ your_string|split:"\n\n" }}
    """
    if not isinstance(value, str):
        return []
    return value.split(sep)
