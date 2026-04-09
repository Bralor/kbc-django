# blog/templatetags/blog_filters.py
from django import template

register = template.Library()


@register.filter
def upper_surname(text: str):
    """Get the upper surname from the text."""
    try:
        first_name, last_name = text.split(' ')
        return ' '.join([first_name, last_name.upper()])
    
    except IndexError:
        return text.upper()
