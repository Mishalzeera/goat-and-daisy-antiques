from django import forms
from . import models

class ShopCheckoutForm(forms.ModelForm):
    class Meta:
        model = models.ShopCustomerInvoice
        exclude = ['notes', 'is_completed', 'paid_on', 'shipping_cost', 'order_amount', 'order_total']