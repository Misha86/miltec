# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def price_exchange(value, arg):
    new_price = Decimal(value*arg).quantize(Decimal("0.00"))
    return new_price