from django.db import models
from shop.models import ShopItems
from repairs_restorals.models import ServiceTicket
import secrets
import datetime

from shop.models import ShopItems


class BaseInvoice(models.Model):
    '''
    Base class of invoice that Shop Customer Invoice and Workshop Customer Invoice inherit from.
    '''
    order_number = models.CharField(max_length=100, editable=False)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=40, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    country = models.CharField(max_length=40, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    order_amount = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    order_total = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)
    paid_on = models.DateTimeField(null=True, blank=True)

    # Generate a unique id using the secrets module
    def _generate_order_number(self):
        return secrets.token_hex(16).upper()

    # Generate a timestamp for when any payments occur
    def _generate_timestamp(self):
        return datetime.datetime.now()

    # If a unique id doesn't exist, create one and save it
    # Add the shipping to the order amount to get the order total
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        self.order_total = self.shipping_cost + self.order_amount
        super().save(*args, **kwargs)


class ShopCustomerInvoice(BaseInvoice):
    '''
    This invoice is for a single payment related to shop items.
    '''

    def __str__(self):
        return self.full_name + "'s Shop Order " + self.order_number


class WorkshopCustomerInvoice(BaseInvoice):
    '''
    This invoice is for two or more payments that are related to individual service tickets.
    '''
    PAYMENT_CHOICES = [
        ('DEP', 'Deposit'),
        ('EP', 'End Payment'),
        ('SPT', 'Single Payment Total'),
        ('SP', 'Supplementary Payment'),
    ]
    payment_type = models.CharField(max_length=25, choices=PAYMENT_CHOICES)
    installment_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name + "'s Workshop Invoice " + self.order_number


class ShopLineItems(models.Model):
    '''
    A line items class related to a Shop Customer Invoice, which is more like
    a typical sales flow - multiple items and subtotals.
    '''
    order = models.ForeignKey(
        ShopCustomerInvoice, on_delete=models.PROTECT, related_name='line_items')
    shop_item = models.ForeignKey(ShopItems, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    line_item_total = models.DecimalField(
        max_digits=6, decimal_places=2, editable=False)

    # When the object is saved, the total is updated
    def save(self, *args, **kwargs):
        self.line_item_total = self.shop_item.price * self.quantity
        super().save(self, *args, **kwargs)
