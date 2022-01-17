from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from .models import ShopItems, ShopItemPhoto


class ShopFront(ListView):
    '''
    A view to return all the antiques for sale
    '''
    model = ShopItems
    template_name = 'shop/shop.html'
    context_object_name = "products"

    # def get(self, request, *args, **kwargs):
    #     return render(request, 'shop/shop.html')


class ShopItem(DetailView):
    ''' 
    A view to return a specific item with options to buy
    '''
    model = ShopItems
    template_name = 'shop/product_detail.html'
    context_object_name = 'item'

    # def get(self, request, *args, **kwargs):
    #     return render(request, 'shop/product_detail.html')
