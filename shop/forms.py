from django.forms import ModelForm
from .models import ShopItemImage, ShopItems


class StaffCreateItemForm(ModelForm):
    class Meta:
        model = ShopItems
        fields = ['title', 'description', 'price']


class StaffImageUploadForm(ModelForm):
    class Meta:
        model = ShopItemImage
        fields = ['product', 'image', ]
