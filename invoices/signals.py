from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WorkshopCustomerInvoice
from repairs_restorals.models import ServiceTicket


@receiver(post_save, sender=ServiceTicket)
def generate_invoice_and_set_has_invoice(sender, instance, created, **kwargs):
    '''
    When a Service Ticket is created, an invoice for a deposit is automatically
    created
    '''
    WorkshopCustomerInvoice.objects.create(service_ticket__id=instance.id)
    instance.set_has_invoice_to_true()
    instance.save()
