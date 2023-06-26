from django.template import Library

from utils.format_price import format_price_to_real

register = Library()


@register.filter
def format_price(value):
    return format_price_to_real(value)
