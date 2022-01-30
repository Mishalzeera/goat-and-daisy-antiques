from django.conf import settings
from decimal import Decimal


def shopping_cart(request):

    template_cart = []
    products_count = 0
    order_amount = 0
    shipping = 0
    order_total = 0

    for item in enumerate(template_cart):
        products_count += 1

    order_total = order_amount + shipping

    context = {
        'template_cart': template_cart,
        'products_count': products_count,
        'order_amount': order_amount,
        'shipping': shipping,
        'order_total': order_total,
    }
    return context
