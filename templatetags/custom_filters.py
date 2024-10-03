# my_app/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retrieve an item from a dictionary using a key."""
    return dictionary.get(key)
