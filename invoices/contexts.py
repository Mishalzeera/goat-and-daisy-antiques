from django.conf import settings
from decimal import Decimal


def shopping_cart(request):

    template_cart = []
    products_count = 0
    order_amount = 120
    shipping =50
    order_total = 0

    for item in enumerate(template_cart):
        products_count += 1

    order_total = order_amount + shipping
    stripe_total = order_total * 100

    context = {
        'template_cart': template_cart,
        'products_count': products_count,
        'order_amount': order_amount,
        'shipping': shipping,
        'order_total': order_total,
        'stripe_total': stripe_total,
    }
    return context
