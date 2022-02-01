from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from shop.models import ShopItems
from .forms import ShopCheckoutForm
import stripe
import json
import os 


stripe.api_key = 'sk_test_51K6Bx2KWJYXuFKtg4k8HIZxsniFPJU3ks7vsbHWwwmBVHk8rRpFxEfIsZa3lyA3bPgNVGP5YY6HgYKirtsCy1D51005zVVT0Gv'


def view_cart(request):
    '''
    Shows the users shopping cart, with items and checkout button.
    '''
    context = {

        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "stripe_secret_key": settings.STRIPE_SECRET_KEY,

    }

    return render(request, 'invoices/shopping_cart.html', context)


def add_to_cart(request, item_id):

    pass

def checkout(request):
    form = ShopCheckoutForm()
    context = {
        'form': form,
        # 'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        # 'client_secret': settings.STRIPE_SECRET_KEY,
    }
    return render(request, 'invoices/checkout.html', context)


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

@require_POST
def create_shop_checkout_session(request):

    data = json.loads(request.body)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(data['items']),
        currency='eur',
        automatic_payment_methods={
            'enabled': True,
        },
    )
    return JsonResponse({
        'clientSecret': intent['client_secret']
    })