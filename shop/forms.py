from django.forms import ModelForm
from .models import ShopItems


class StaffCreateItemForm(ModelForm):
    class Meta:
        model = ShopItems
        fields =  ['title', 'description', 'price']