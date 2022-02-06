from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages
from django.views.decorators.http import require_POST
from shop.models import ShopItems
from profiles.models import Customer
from .forms import ShopCheckoutForm
# from .contexts import shopping_cart
import stripe
import json
import os 


stripe.api_key = 'sk_test_51K6Bx2KWJYXuFKtg4k8HIZxsniFPJU3ks7vsbHWwwmBVHk8rRpFxEfIsZa3lyA3bPgNVGP5YY6HgYKirtsCy1D51005zVVT0Gv'


def view_cart(request):
    '''
    Shows the users shopping cart, with items and checkout button.
    '''
    context = {

        # "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        # "stripe_secret_key": settings.STRIPE_SECRET_KEY,

    }

    return render(request, 'invoices/shopping_cart.html', context)


def add_to_cart(request, item_id):
    
    
    item = get_object_or_404(ShopItems, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    id = item.id
    cart = request.session.get('cart', {})
    
    
    cart[str(item_id)] = dict(id=item_id)
    
    request.session['cart'] = cart

    messages.success(request, (f"Successfully added {item.title} to your shopping cart."))

    return redirect(redirect_url)


def remove_from_cart(request, item_id):
        
    item = get_object_or_404(ShopItems, pk=item_id)
    id = item.id
    cart = request.session.get('cart', {})
    
    
    cart.pop(str(item_id))
    
    request.session['cart'] = cart

    messages.success(request, (f"Successfully removed {item.title} from your shopping cart."))

    return redirect('view_cart')

def checkout(request):

    if request.user.is_authenticated:
        customer_profile = get_object_or_404(Customer, username=request.user)
    else:
        customer_profile = {"full_name": "Not authenticated"}

    

    form = ShopCheckoutForm()
    context = {
        'form': form,
        'customer_profile': customer_profile,
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