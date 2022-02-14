from django.http import HttpResponse
from django.core.mail import send_mail
from .models import ShopCustomerInvoice, WorkshopCustomerInvoice
from profiles.models import Customer
from shop.models import ShopItems
import datetime
import time 

class StripeWebhookHandlerSHOP:

    def __init__(self, request, order_number, shopping_cart, customer_email):
        self.request = request 
        self.order_number = order_number
        self.shopping_cart = shopping_cart
        self.customer_email = customer_email
        

    def handle_event(self, event):
        print("THIS IS AN UNKNOWN EVENT")
        return HttpResponse(
            content = f'Unhandled Webhook received {event["type"]}',
            status = 200
            )
        
    def handle_payment_intent_suceeded(self, event):

        print("THIS IS A SUCCESSFUL SHOP ORDER")
        invoice_exists = False 
        attempt = 1
        while attempt <= 5:
            try:
                # Get the invoice
                this_invoice = ShopCustomerInvoice.objects.get(order_number=self.order_number)
                invoice_exists = True
                break
            except ShopCustomerInvoice.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if invoice_exists:
            # We take the item/s off the inventory 
            # Create an empty shopping list
            shopping_list = []
            # ..using the shopping cart ids from the webhooks function
            # ...iterate over the items in the shopping cart
            for item_id in self.shopping_cart:
                # ...populate the shopping list with the purchased items
                shopping_list.append(ShopItems.objects.get(id=item_id))
            
            # ...iterating over the shopping list, set each item to unavailable
            # ...taking them out of the shop
            for shopitem in shopping_list:
                shopitem.is_available = False
                shopitem.save()
                # and adding the item title to the invoice notes for the shop
                # staff
                this_invoice.notes += shopitem.title + " - "
                this_invoice.save()
            

            

            # We mark the transaction as paid, so staff can ship it
            this_invoice.paid_on = datetime.datetime.now()
            this_invoice.save()

            # We send a confirmation email to the customer 

            send_mail(
                subject = (f"Confirmation for {this_invoice}."),
                message = (f"Thank you for your purchase. Our staff are putting your order together now. Please contact us at +1 818-455-9778 if you have any concerns or questions."),
                recipient_list = [self.customer_email],
                from_email = "shop@goat-and-daisy.com",
            )

            return HttpResponse(
                content = f'Webhook received {event["type"]}',
                status = 200
                )

        else: 
            return HttpResponse(
                content = f'No invoice found',
                status = 400
            )

            

    def handle_payment_intent_payment_failed(self, event):
        print("THIS IS A FAILED SHOP ORDER")
        # Put the item back in the inventory

        # Set the invoice to incomplete, to avoid any accidents 

        this_invoice = ShopCustomerInvoice.objects.get(order_number=self.order_number)
        this_invoice.is_completed = False
        this_invoice.save()

        # Send an email to the customer
        send_mail(
            subject = (f"Error with order {this_invoice}."),
            message = (f"There was an error with your payment. Please contact our staff at +1 818-656-7888 for assistance."),
            recipient_list = [self.customer_email],
            from_email = "shop@goat-and-daisy.com",
        )
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

class StripeWebhookHandlerWORKSHOP:

    def __init__(self, request, order_number, invoice_type, customer_email):
        self.request = request 
        self.order_number = order_number
        self.invoice_type = invoice_type
        self.customer_email = customer_email

    def handle_event(self, event):
        print("THIS IS AN UNKNOWN WORKSHOP EVENT")
        return HttpResponse(
            content = f'Unhandled Webhook received {event["type"]}',
            status = 200
            )
        
    def handle_payment_intent_suceeded(self, event):
        print("THIS IS A SUCCESSFUL WORKSHOP ORDER")
        print(self.customer_email)
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
            
            # Send email confirmation
            send_mail(
            subject = (f"Confirmation for {this_invoice}."),
            message = "Thank you for your payment. Your bill for our work is paid in full.",
            recipient_list = [self.customer_email],
            from_email = "workshop@goat-and-daisy.com",
            )

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

            # Send the customer email confirmation 
            send_mail(
            subject = (f"Confirmation for {this_invoice}."),
            message = "Thank you for your payment. We will begin work on your project presently. We will contact you soon for an update.",
            recipient_list = [self.customer_email],
            from_email = "workshop@goat-and-daisy.com",
            )

        if self.invoice_type == "SP":

            # Send the customer email confirmation 
            send_mail(
            subject = (f"Confirmation for {this_invoice}."),
            message = "Thank you for your payment. Please check your Workbench for any updates. ",
            recipient_list = [self.customer_email],
            from_email = "workshop@goat-and-daisy.com",
            )

        
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
    
    
