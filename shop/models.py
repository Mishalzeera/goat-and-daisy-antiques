from django.db import models


class ShopItems(models.Model):
    '''
    Models the items for sale in the shop. Fields are image, name, description,
    price, is_available, image_url 
    '''
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=12)


class ShopItemPhoto(models.Model):
    '''
    Photos linked to an instance of ShopItem class
    '''
    linked_item = models.ForeignKey(ShopItems, on_delete=models.CASCADE)
    image = models.ImageField()

