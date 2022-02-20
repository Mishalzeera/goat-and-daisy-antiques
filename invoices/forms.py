from django import forms
from . import models


class ShopCheckoutForm(forms.ModelForm):
    """
    Checkout form for when a shop customer pays.
    """
    class Meta:
        model = models.ShopCustomerInvoice
        exclude = ['notes', 'is_completed', 'paid_on',
                   'shipping_cost', 'order_amount', 'order_total']

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.fields['full_name'].required = True
        self.fields['email'].required = True
        self.fields['address1'].required = True
        self.fields['postcode'].required = True
        self.fields['town_or_city'].required = True
        self.fields['country'].required = True
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'address1': 'Address 1',
            'address2': 'Address 2',
            'postcode': 'Postal Code',
            'town_or_city': 'Town Or City',
            'country': 'Country',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
