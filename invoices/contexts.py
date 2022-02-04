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
    # You have to refer to a [key] not a [index_num]
    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            shop_item = get_object_or_404(ShopItems, pk=item_data)
            to_append = {
                'id': shop_item.id,
                'title': shop_item.title,
                'price': float(shop_item.price),
            }

            if not to_append in template_cart:
                template_cart.append(to_append)
                order_amount += float(shop_item.price)

  
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
