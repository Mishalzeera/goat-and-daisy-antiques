import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShopItemImage, ShopItems


# @receiver(post_save, sender=ShopItems)
# def set_first_image_to_primary(sender, instance, created, **kwargs):
#     '''
#     When a ShopItem is saved, if there is only one image, it will be set to
#     default
#     '''
    # image_set = ShopItemImage.objects.filter(product__id=instance.id)


        
