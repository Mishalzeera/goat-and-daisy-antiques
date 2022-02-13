from django.db import models
from profiles.models import Customer


class ShopItems(models.Model):
    '''
    Models the items for sale in the shop. 
    '''
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=12)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Shop Items"


class ShopItemImage(models.Model):
    '''
    Photos linked to an instance of ShopItem class.
    '''
    product = models.ForeignKey(
        ShopItems, on_delete=models.CASCADE, related_name='images')
    is_primary_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to='shop/images')

    def __str__(self) -> str:
        return str(self.product) + str(self.id)



