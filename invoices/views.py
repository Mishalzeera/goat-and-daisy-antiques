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
from .models import ShopCustomerInvoice, WorkshopCustomerInvoice
import datetime
# from .contexts import shopping_cart
import stripe
import json
import time 
from threading import Thread, Timer
import os 


stripe.api_key = settings.STRIPE_SECRET_KEY


def view_cart(request):
    '''
    Shows the users shopping cart, with items and checkout button.
    '''
    context = {



    }

    return render(request, 'invoices/shopping_cart.html', context)


def timer(item_id):
    '''
    Timer for the hold function. Occurs in its own thread, which is 
    instantiated in the toggle function. 
    '''
    time.sleep(settings.CUSTOMER_SESSION_EXPIRY)
    release_shop_item(item_id)


def hold_shop_item(item_id):
    '''
    Function that starts a timer, taking a shop item off the shop
    for length of time specified in settings.CUSTOMER_SESSION_EXPIRY.
    '''
    
    item = get_object_or_404(ShopItems, pk=item_id)
    if item.is_available:
        
        item.is_available = False
        item.save()
        timer_thread = Thread(target=timer, args=(item_id,), daemon=True)
        timer_thread.start()
   

def release_shop_item(item_id):
    '''
    Releases an object back to the shop to be purchased by another customer.
    '''
    item = get_object_or_404(ShopItems, pk=item_id)

    if item.is_available == False:
        item.is_available = True
        item.save()



def add_to_cart(request, item_id):
    '''
    Adds a shop item to the session shopping cart.
    '''
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


def remove_from_cart(request, item_id):
    '''
    Removes an item from the session shopping cart.
    '''
        
    item = get_object_or_404(ShopItems, pk=item_id)
    id = item.id
    cart = request.session.get('cart', {})
    
    
    cart.pop(str(item_id))
    
    request.session['cart'] = cart

    release_shop_item(item_id)

    messages.success(request, (f"Successfully removed {item.title} from your shopping cart."))

    return redirect('view_cart')


def precheckout(request):
    '''
    Creates an invoice in the system for a shop customer, and confirms the 
    shipping address for the order. 
    '''
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
            )
            
            new_invoice.save()
            request.session['shop_order_number'] = new_invoice.order_number
            request.session['shop_or_workshop'] = "Shop"



        else:
            form = ShopCheckoutForm(request.POST)
            if form.is_valid():
                form.instance.order_amount = order_amount
                form.instance.shipping_cost = shipping_cost
                form.instance.order_total = order_total 
                form.instance.notes = "This customer does not have an account."
                form.save()
                request.session['shop_order_number'] = form.instance.order_number
                request.session['shop_or_workshop'] = "Shop"



            else:

                messages.error(request, ("Form not filled correctly"))


        return redirect('checkout')


def checkout(request):


    if request.user.is_authenticated:
        customer_profile = get_object_or_404(Customer, username=request.user)
    else:
        customer_profile = {"full_name": "Not authenticated"}

    

    form = ShopCheckoutForm()
    context = {
        'customer_profile': customer_profile,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'invoices/checkout.html', context)




def workshop_checkout(request, invoice_id):
    '''
    Allows a workshop client to pay their invoices. Use the deposit amount
    to calculate the end payment amount for the newly created object.
    '''

    # The relevant customer and invoice are gotten
    customer = Customer.objects.get(username=request.user)
    invoice = WorkshopCustomerInvoice.objects.get(pk=invoice_id)

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
    
    context = {
        'invoice': invoice,
        'stripe_order_total': stripe_order_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'customer': customer,
    }        

    return render(request, 'invoices/workshop_checkout.html', context)

    # For WEBHOOOK
    # if request.method == 'POST':

    #     payment_type = request.POST['payment_type']

    #     # ...apply the datestamp
    #     invoice.paid_on = datetime.datetime.now()

    #     # If the payment is a deposit (DEP) or supplementary payment(SP)
    #     if payment_type == 'DEP' or payment_type == 'SP':

    #         # ... the payment is counted as a paid installment, but not 
    #         # completed
    #         invoice.installment_paid = True
    #         invoice.save()

    #     # ... else if it is an endpayment (EP) or single payment total (SPT)
    #     elif payment_type == 'EP' or payment_type == 'SPT': 

    #         # For consistency, is paid as an installment
    #         invoice.installment_paid = True
    #         invoice.save()

    #         # All related invoices are set to 'is_completed'
    #         related_invoices = WorkshopCustomerInvoice.objects.filter(service_ticket_id = invoice.service_ticket_id)

    #         for invoice in related_invoices:
    #             invoice.is_completed = True
    #             invoice.save()

    #     # If the payment was a deposit, an end payment invoice is created in
    #     # the customers account
    #     if payment_type == 'DEP':
    #         final_invoice = WorkshopCustomerInvoice.objects.create(
    #             service_ticket_id = invoice.service_ticket_id,
    #             full_name=customer.full_name,
    #             email=customer.email,
    #             address1=customer.address1,
    #             address2=customer.address2,
    #             postcode=customer.postcode,
    #             town_or_city=customer.town_or_city,
    #             country=customer.country,
    #             payment_type='EP',

    #         )
    #         final_invoice.save()
        


        
        
    #     messages.success(request, ("Thank you, you have paid."))
    #     return redirect('workshop')
        

def calculate_order_amount(cart):
    # Cart comes from the JS file initialize() function. Sent from a 
    sum = cart[0]['total']
    return sum 

@require_POST
def create_checkout_session(request):

    # Check the type of service 
    if request.session['shop_or_workshop'] == 'Workshop':
        # create metadata dictionaries to send to Stripe
        metadata = {
            'shop_or_workshop': request.session['shop_or_workshop'],
            'unique_order_number': request.session['workshop_order_number'],
            'invoice_type': request.session['invoice_type'],

        }

    elif request.session['shop_or_workshop'] =='Shop':
        metadata = {
            'shop_or_workshop': request.session['shop_or_workshop'],
            'unique_order_number': request.session['shop_order_number'],
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