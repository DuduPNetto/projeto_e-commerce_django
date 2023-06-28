from django.template import Library

from utils.cart_total_quantity import cart_total_quantity
from utils.format_price import format_price_to_real

register = Library()


@register.filter
def format_price(value):
    return format_price_to_real(value)


@register.filter
def cart_total(cart):
    return cart_total_quantity(cart)
