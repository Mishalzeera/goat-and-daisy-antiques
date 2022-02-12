from django.http import HttpResponse
from .models import ShopCustomerInvoice, WorkshopCustomerInvoice
from profiles.models import Customer
import datetime

class StripeWebhookHandlerSHOP:

    def __init__(self, request, order_number):
        self.request = request 
        self.order_number = order_number
        

    def handle_event(self, event):
        print("THIS IS AN UNKNOWN EVENT")
        return HttpResponse(
            content = f'Unhandled Webhook received {event["type"]}',
            status = 200
            )
        
    def handle_payment_intent_suceeded(self, event):

        print("THIS IS A SUCCESSFUL SHOP ORDER")

        # We take the item off the inventory

        # We mark the transaction as paid, so staff can ship it

        this_invoice = ShopCustomerInvoice.objects.get(order_number=self.order_number)
        this_invoice.is_completed = True
        this_invoice.save()

        # We send a confirmation email to the customer 

        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

    def handle_payment_intent_payment_failed(self, event):
        print("THIS IS A FAILED SHOP ORDER")
        # Put the item back in the inventory

        # Set the invoice to incomplete 

        this_invoice = ShopCustomerInvoice.objects.get(order_number=self.order_number)
        this_invoice.is_completed = False
        this_invoice.save()

        # Send an email to the customer
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

class StripeWebhookHandlerWORKSHOP:

    def __init__(self, request, order_number, invoice_type):
        self.request = request 
        self.order_number = order_number
        self.invoice_type = invoice_type

    def handle_event(self, event):
        print("THIS IS AN UNKNOWN WORKSHOP EVENT")
        return HttpResponse(
            content = f'Unhandled Webhook received {event["type"]}',
            status = 200
            )
        
    def handle_payment_intent_suceeded(self, event):
        print("THIS IS A SUCCESSFUL WORKSHOP ORDER")

        this_invoice = WorkshopCustomerInvoice.objects.get(order_number=self.order_number)

        # ...apply the datestamp
        this_invoice.paid_on = datetime.datetime.now()

        # If the payment is a deposit (DEP) or supplementary payment(SP)
        if self.invoice_type == 'DEP' or self.invoice_type == 'SP':

            # ... the payment is counted as a paid installment, but not 
            # completed
            this_invoice.installment_paid = True
            this_invoice.save()

        # ... else if it is an endpayment (EP) or single payment total (SPT)
        elif self.invoice_type == 'EP' or self.invoice_type == 'SPT': 

            # For consistency, is paid as an installment
            this_invoice.installment_paid = True
            this_invoice.save()

            # All related invoices are set to 'is_completed'
            related_invoices = WorkshopCustomerInvoice.objects.filter(service_ticket_id = this_invoice.service_ticket_id)

            for invoice in related_invoices:
                invoice.is_completed = True
                invoice.save()

        # If the payment was a deposit, an end payment invoice is created in
        # the customers account
        customer = Customer.objects.get(username=this_invoice.service_ticket.customer.username)
        if self.invoice_type == 'DEP':
            final_invoice = WorkshopCustomerInvoice.objects.create(
                service_ticket_id = this_invoice.service_ticket_id,
                full_name=customer.full_name,
                email=customer.email,
                address1=customer.address1,
                address2=customer.address2,
                postcode=customer.postcode,
                town_or_city=customer.town_or_city,
                country=customer.country,
                payment_type='EP',

            )
            final_invoice.save()


        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

    def handle_payment_intent_payment_failed(self, event):
        print("THIS IS An UNSUCCESSFUL WORKSHOP ORDER")
        this_invoice = WorkshopCustomerInvoice.objects.get(order_number=self.order_number)
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )
    
    
