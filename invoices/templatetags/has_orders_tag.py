from django import template

register = template.Library()


@register.filter(name='has_shop_orders')
def has_shop_orders(request):
    try:
        if request.session['cart']:
            return True


    except request.session['cart'] == {}:

        return False

