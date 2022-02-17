from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from shop.models import ShopItems
from profiles.models import Customer
from .forms import ShopCheckoutForm
from .models import ShopCustomerInvoice, WorkshopCustomerInvoice
import datetime
# from .contexts import shopping_cart
import stripe
import json
import time 
from threading import Thread, Timer
import os 


stripe.api_key = settings.STRIPE_SECRET_KEY

# public
def view_cart(request):
    """
    Shows the users shopping cart, with items and checkout button.
    """
    context = {



    }

    return render(request, 'invoices/shopping_cart.html', context)

# inner function
def timer(item_id):
    """
    Timer for the hold function. Occurs in its own thread, which is 
    instantiated in the toggle function. 
    """
    time.sleep(settings.CUSTOMER_SESSION_EXPIRY)
    release_shop_item(item_id)

# public
def hold_shop_item(item_id):
    """
    Function that starts a timer, taking a shop item off the shop
    for length of time specified in settings.CUSTOMER_SESSION_EXPIRY.
    """
    
    item = get_object_or_404(ShopItems, pk=item_id)
    if item.is_available:
        
        item.is_available = False
        item.save()
        timer_thread = Thread(target=timer, args=(item_id,), daemon=True)
        timer_thread.start()
   
# public
def release_shop_item(item_id):
    """
    Releases an object back to the shop to be purchased by another customer.
    """
    item = get_object_or_404(ShopItems, pk=item_id)

    if item.is_available == False:
        item.is_available = True
        item.save()

# public
def add_to_cart(request, item_id):
    """
    Adds a shop item to the session shopping cart.
    """
    item = get_object_or_404(ShopItems, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    id = item.id
    cart = request.session.get('cart', {})
    
    
    cart[str(item_id)] = dict(id=item_id)
    
    
    request.session['cart'] = cart
    request.session.set_expiry(settings.CUSTOMER_SESSION_EXPIRY)
    hold_shop_item(item_id)


    messages.success(request, (f"Successfully added {item.title} to your shopping cart."))

    return redirect(redirect_url)

# public
def remove_from_cart(request, item_id):
    """
    Removes an item from the session shopping cart.
    """
        
    item = get_object_or_404(ShopItems, pk=item_id)
    id = item.id
    cart = request.session.get('cart', {})
    
    
    cart.pop(str(item_id))
    
    request.session['cart'] = cart

    release_shop_item(item_id)

    messages.success(request, (f"Successfully removed {item.title} from your shopping cart."))

    return redirect('view_cart')

# public
def precheckout(request):
    """
    Creates an invoice in the system for a shop customer, and confirms the 
    shipping address for the order. 
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            customer_profile = get_object_or_404(Customer, username=request.user)
        else:
            customer_profile = {"full_name": "Not authenticated"}

        form = ShopCheckoutForm()
        context = {
            'form': form,
            'customer_profile': customer_profile,
        }

        return render(request, 'invoices/precheckout.html', context)
    
    if request.method == "POST":

        order_amount = request.POST.get('order_amount')
        shipping_cost = request.POST.get('shipping')
        order_total = request.POST.get('order_total')

        if request.user.is_authenticated:
            customer_profile = get_object_or_404(Customer, username=request.user)
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
                notes = '',
            )
            
            new_invoice.save()
            customer_profile.has_active_shop_orders = True
            customer_profile.save()
            request.session['shop_order_number'] = new_invoice.order_number
            request.session['shop_or_workshop'] = "Shop"
            request.session['customer_full_name'] = new_invoice.full_name
            request.session['customer_email'] = new_invoice.email
            request.session['customer_address1'] = request.POST.get('address1')
            request.session['customer_address2'] = request.POST.get('address2')
            request.session['customer_postcode'] = request.POST.get('postcode')
            request.session['customer_town_or_city'] = request.POST.get('town_or_city')
            request.session['customer_country'] = request.POST.get('country')

            request.session['shopping_cart'] = ''
            cart = request.session.get('cart', {})

            for item_id, item_value in cart.items():
                for key, value in item_value.items():
                    to_concatenate = str(value)
                    request.session['shopping_cart'] += to_concatenate + " "

            
            # request.session['cart'] = {}



        else:
            form = ShopCheckoutForm(request.POST)
            if form.is_valid():
                form.instance.order_amount = order_amount
                form.instance.shipping_cost = shipping_cost
                form.instance.order_total = order_total 
                form.instance.notes = "Note: This customer does not have an account."
                form.save()
                request.session['shop_order_number'] = form.instance.order_number
                request.session['shop_or_workshop'] = "Shop"
                request.session['customer_full_name'] = form.instance.full_name
                request.session['customer_email'] = form.instance.email
                request.session['customer_address1'] = form.instance.address1
                request.session['customer_address2'] = form.instance.address2
                request.session['customer_postcode'] = form.instance.postcode
                request.session['customer_town_or_city'] = form.instance.town_or_city
                request.session['customer_country'] = form.instance.country
                request.session['shopping_cart'] = ''
                cart = request.session.get('cart', {})

                for item_id, item_value in cart.items():
                    for key, value in item_value.items():
                        to_concatenate = str(value)
                        request.session['shopping_cart'] += to_concatenate + " "
                
                # request.session['cart'] = {}


            else:

                messages.error(request, ("Form not filled correctly"))


        return redirect('checkout')

# public
def checkout(request):
    """
    Checkout for a shop purchase.
    """

    if request.user.is_authenticated:
        customer_profile = get_object_or_404(Customer, username=request.user)
    else:
        customer_profile = {"full_name": "Not authenticated"}

    form = ShopCheckoutForm()
    context = {
        'customer_profile': customer_profile,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'stripe_base_url': settings.STRIPE_BASE_URL,
    }
    return render(request, 'invoices/checkout.html', context)

# login required
@login_required
def workshop_checkout(request, invoice_id):
    """
    Allows a workshop client to pay their invoices. Use the deposit amount
    to calculate the end payment amount for the newly created object.
    """

    # The relevant customer and invoice are gotten
    customer = Customer.objects.get(username=request.user)
    invoice = WorkshopCustomerInvoice.objects.get(pk=invoice_id)
    zero_error = None

    # ... and sent to the template
    stripe_order_total = round(invoice.order_total * 100)

    if stripe_order_total <= 0:
        zero_error = "Please contact a staff member to process your invoice before payment."
    
    # storing the type of service
    request.session['shop_or_workshop'] = "Workshop"
    # storing the type of invoice
    request.session['invoice_type'] = invoice.payment_type
    # storing the order number in a session variable
    request.session['workshop_order_number'] = invoice.order_number
    # storing the name
    request.session['customer_full_name'] = invoice.full_name
    # storing the email address in a session variable
    request.session['customer_email'] = customer.email
    
    context = {
        'invoice': invoice,
        'stripe_order_total': stripe_order_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'stripe_base_url': settings.STRIPE_BASE_URL,
        'customer': customer,
        'zero_error': zero_error,
    }        

    return render(request, 'invoices/workshop_checkout.html', context)

# public
def success(request):
    """
    The redirect for a successful payment. 
    """
    shopping_list = None
    customer_address1 = None
    customer_address2 = None
    customer_postcode = None
    customer_town_or_city = None
    customer_country = None
    message = None

    if request.session['shop_or_workshop'] == "Shop":
        order_number = request.session['shop_order_number']

        customer_address1 = request.session['customer_address1'] 
        customer_address2 = request.session['customer_address2']
        customer_postcode = request.session['customer_postcode'] 
        customer_town_or_city = request.session['customer_town_or_city'] 
        customer_country = request.session['customer_country'] 
        message = "Here is a list of purchased items, and the address we will be shipping to: "
        # Create an list using the white spaces as delimiter
        string_cart = request.session['shopping_cart'].split(" ")
        # Getting the whitespaces out by filtering out None values
        no_none_cart = [*filter(None, string_cart)]
        # Converting the result into integers for the handler
        shopping_cart = [int(item) for item in no_none_cart]
        shopping_list = []
        # Iterate over the items in the shopping cart
        for item_id in shopping_cart:
            # ...populate the shopping list with the purchased items
            shopping_list.append(ShopItems.objects.get(id=item_id))

    elif request.session['shop_or_workshop'] == "Workshop":
        order_number = request.session['workshop_order_number']
        customer = get_object_or_404(Customer, username=request.user)
        customer_address1 = customer.address1
        customer_address2 = customer.address2
        customer_postcode = customer.postcode
        customer_town_or_city = customer.town_or_city
        customer_country = customer.country
        message = "You have paid. These are your current shipping details, please keep them up to date."




    context = {

        'order_number': order_number,
        'customer_full_name': request.session['customer_full_name'],
        'customer_email': request.session['customer_email'],
        'customer_address1': customer_address1,
        'customer_address2': customer_address2,
        'customer_postcode': customer_postcode,
        'customer_town_or_city': customer_town_or_city,
        'customer_country': customer_country,
        'shopping_list': shopping_list,
        'message': message, 


    }

    request.session['cart'] = {}

    return render(request, 'invoices/success.html', context)

# inner function
def calculate_order_amount(cart):
    """
    Gets an updated total from the checkout page.
    """
    # Cart comes from the JS file initialize() function.  
    sum = cart[0]['total']
    return sum 

# public
@require_POST
def create_checkout_session(request):
    """
    Adapted from Stripe docs, modified with pertinent metadata for webhooks.py
    and webhook_handler.py to use.
    """
    # Check the type of service 
    if request.session['shop_or_workshop'] == 'Workshop':
        # create metadata dictionaries to send to Stripe
        metadata = {
            'shop_or_workshop': request.session['shop_or_workshop'],
            'unique_order_number': request.session['workshop_order_number'],
            'invoice_type': request.session['invoice_type'],
            'customer_email': request.session['customer_email'],

        }

    elif request.session['shop_or_workshop'] =='Shop':
        metadata = {
            'shop_or_workshop': request.session['shop_or_workshop'],
            'unique_order_number': request.session['shop_order_number'],
            'shopping_cart': request.session['shopping_cart'],
            'customer_email': request.session['customer_email'],
        }

    data = json.loads(request.body)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(data['cart']),
        currency='eur',
        automatic_payment_methods={
            'enabled': True,
        },
        # This metadata insertion allows us to access invoice details in the
        # webhook handler
        metadata = metadata,
    )
    return JsonResponse({
        'clientSecret': intent['client_secret']
    })