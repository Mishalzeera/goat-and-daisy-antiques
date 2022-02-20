from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import WorkshopCustomerInvoice
from profiles.models import Customer
from repairs_restorals.models import ServiceTicket


@receiver(post_save, sender=ServiceTicket)
def generate_invoice_and_set_has_invoice(sender, instance, created, **kwargs):
    """
    When a Service Ticket is created, an invoice for a deposit is automatically
    created
    """
    if not WorkshopCustomerInvoice.objects.filter(service_ticket_id=instance.id):
        customer = Customer.objects.get(username=instance.customer.username)

        WorkshopCustomerInvoice.objects.create(
            service_ticket_id=instance.id,
            full_name=customer.full_name,
            email=customer.email,
            address1=customer.address1,
            address2=customer.address2,
            postcode=customer.postcode,
            town_or_city=customer.town_or_city,
            country=customer.country,
            payment_type='DEP',

        )
        instance.set_has_invoice_to_true()
        instance.save()

        send_mail(
            subject=(f"Thank you, {customer.full_name}."),
            message=(f"Thank you for creating your service ticket. Our staff is reviewing your request. An invoice for your deposit of 50% will be in your Workbench at www.goat-and-daisy.com/workshop within two weeks. Please call us at 818-657-8181 if you have any questions."),
            recipient_list=[customer.email],
            from_email="workshop@goat-and-daisy.com",
        )
