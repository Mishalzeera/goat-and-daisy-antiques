from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages


class ShopFront(View):
    '''
    A view to return all the antiques for sale
    '''
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/shop.html')


class ShopItem(View):
    ''' 
    A view to return a specific item with options to buy
    '''
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/product_detail.html')
