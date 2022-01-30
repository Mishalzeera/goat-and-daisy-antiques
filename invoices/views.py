from django.shortcuts import render, redirect
from .contexts import shopping_cart


def add_to_cart(request):

    cart = request.session.get('shopping_cart', {})

    context = {
        'cart': cart,
    }

    return render(request, 'invoices/shopping_cart.html', context)
