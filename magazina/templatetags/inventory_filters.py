from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter
def sasi_format(value, njesia):
    try:
        number = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value

    if njesia != 'KG':
        return str(number.quantize(Decimal('1')))

    normalized = number.normalize()
    return format(normalized, 'f')
