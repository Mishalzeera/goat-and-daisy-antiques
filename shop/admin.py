from django.contrib import admin
from .models import ShopItems, ShopItemImage

admin.site.register(ShopItemImage)


@admin.register(ShopItems)
class ShopItemsAdmin(admin.ModelAdmin):
    list_display = ['title', 'Price']

    def Price(self, shopitems):
        return "EU " + str(shopitems.price)
