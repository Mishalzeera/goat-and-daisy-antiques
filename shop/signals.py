import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from invoices.models import ShopCustomerInvoice


@receiver(post_save, sender=ShopCustomerInvoice)
def generate_invoice_and_set_has_invoice(sender, instance, created, **kwargs):
    '''
    When a Service Ticket is created, an invoice for a deposit is automatically
    created
    '''
    if not ShopCustomerInvoice.objects.filter(service_ticket_id=instance.id):
        customer = Customer.objects.get(username=instance.customer.username)

        ShopCustomerInvoice.objects.create(
            service_ticket_id=instance.id,
            full_name=customer.full_name,
            payment_type='DEP',

        )
        instance.set_has_invoice_to_true()
        instance.save()
