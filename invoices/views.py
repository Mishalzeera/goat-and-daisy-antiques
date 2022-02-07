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
from .models import ShopCustomerInvoice
# from .contexts import shopping_cart
import stripe
import json
import time 
from threading import Thread, Timer
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

def timer(item_id):
    '''
    Timer for the toggle function below. Occurs in its own thread, which is 
    instantiated in the toggle function. 
    '''
    time.sleep(600)
    toggle_hold_shop_item(item_id)


def toggle_hold_shop_item(item_id):
    '''
    Function that toggles a 10 minute timer, taking a shop item off the shop
    for 10 minutes and adding it back in when the customer removes the item
    from cart.
    '''
    
    item = get_object_or_404(ShopItems, pk=item_id)
    if item.is_available:
        
        item.is_available = False
        item.save()
        timer_thread = Thread(target=timer, args=(item_id,), daemon=True)
        timer_thread.start()

    elif item.is_available == False:
            item.is_available = True
            item.save()
    

def add_to_cart(request, item_id):
    
    
    item = get_object_or_404(ShopItems, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    id = item.id
    cart = request.session.get('cart', {})
    
    
    cart[str(item_id)] = dict(id=item_id)
    
    request.session['cart'] = cart

    toggle_hold_shop_item(item_id)

    messages.success(request, (f"Successfully added {item.title} to your shopping cart."))

    return redirect(redirect_url)


def remove_from_cart(request, item_id):
        
    item = get_object_or_404(ShopItems, pk=item_id)
    id = item.id
    cart = request.session.get('cart', {})
    
    
    cart.pop(str(item_id))
    
    request.session['cart'] = cart

    toggle_hold_shop_item(item_id)

    messages.success(request, (f"Successfully removed {item.title} from your shopping cart."))

    return redirect('view_cart')

def checkout(request):

    if request.method == 'GET':

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

    if request.method == 'POST':
        order_amount = request.POST.get('order_amount')
        shipping_cost = request.POST.get('shipping')
        order_total = request.POST.get('order_total')
        if request.user.is_authenticated:


            new_invoice = ShopCustomerInvoice.objects.create(
                full_name= request.POST.get('full_name'),
                email= request.POST.get('email'),
                address1= request.POST.get('address1'),
                address2= request.POST.get('address2'),
                postcode= request.POST.get('postcode'),
                town_or_city= request.POST.get('town_or_city'),
                country= request.POST.get('country'),
                order_amount = order_amount,
                shipping_cost = shipping_cost,
                order_total = order_total,
                is_completed = True,
            )
            
            new_invoice.save()

        else:
            form = ShopCheckoutForm(request.POST)
            if form.is_valid():
                form.instance.is_completed = True
                form.instance.order_amount = order_amount
                form.instance.shipping_cost = shipping_cost
                form.instance.order_total = order_total 
                form.save()
                messages.success(request, ("You have paid, thank you."))
            else:
                messages.error(request, ("Form not filled correctly"))

        
        
        return redirect('index')

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return items 

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