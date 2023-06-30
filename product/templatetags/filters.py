from django.template import Library

from utils.cart_total import cart_total_qtt, cart_totals
from utils.format_price import format_price_to_real

register = Library()


@register.filter
def format_price(value):
    return format_price_to_real(value)


@register.filter
def cart_total_quantity(cart):
    return cart_total_qtt(cart)


@register.filter
def cart_total(cart):
    return cart_totals(cart)
