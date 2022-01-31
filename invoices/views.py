from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .contexts import shopping_cart
from .forms import ShopCheckoutForm
import stripe
import json
import os 


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
    return render(request, 'invoices/checkout.html')