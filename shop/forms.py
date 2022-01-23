from django.forms import ModelForm
from .models import ShopItemImage, ShopItems


class StaffCreateItemForm(ModelForm):
    '''
    Form that allows staff to create an inventory item.
    '''
    class Meta:
        model = ShopItems
        fields = ['title', 'description', 'price']


class StaffImageUploadForm(ModelForm):
    '''
    Form that allows staff to upload inventory images.
    '''
    class Meta:
        model = ShopItemImage
        fields = ['product', 'image', ]
