from django.conf import settings
from django.shortcuts import get_object_or_404
from decimal import Decimal
from shop.models import ShopItems


def shopping_cart(request):

    template_cart = []
    products_count = 0
    order_amount = 0
    shipping = 500
    cart = request.session.get('cart', {})

    for item_id, item_value in cart.items():
        for key, value in item_value.items():

            if isinstance(value, int):
                shop_item = get_object_or_404(ShopItems, pk=value)
                to_append = {
                    'id': shop_item.id,
                    'product': shop_item,
                }


                if not to_append in template_cart:
                    template_cart.append(to_append)
                    order_amount += float(shop_item.price)

    for item in enumerate(template_cart):
        products_count += 1

    order_total = order_amount + shipping
    stripe_total = round(order_total * 100)



    context = {
        'template_cart': template_cart,
        'products_count': products_count,
        'order_amount': order_amount,
        'shipping': shipping,
        'order_total': order_total,
        'stripe_total': stripe_total,
    }


    return context
