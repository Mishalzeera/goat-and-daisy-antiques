from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import ShopItems, ShopItemImage
from .forms import StaffCreateItemForm, StaffImageUploadForm


class ShopFront(ListView):
    '''
    A view to return all the antiques for sale.
    '''
    model = ShopItems
    template_name = 'shop/shop.html'
    queryset = ShopItems.objects.prefetch_related('images').all()
    context_object_name = "products"


class ShopItem(DetailView):
    ''' 
    A view to return a specific item with options to buy.
    '''
    model = ShopItems
    template_name = 'shop/product_detail.html'
    context_object_name = 'item'


class StaffManageItems(ListView):
    '''
    Allows a shop staff member to have an overview of inventory with
    CRUD functionality.
    '''
    model = ShopItems
    template_name = 'shop/staff_manage_items.html'
    queryset = ShopItems.objects.prefetch_related('images').all()
    context_object_name = "products"


class StaffUpdateItem(UpdateView):
    '''
    Allows a shop staff member to change a particular inventory item.
    '''
    model = ShopItems
    form_class = StaffCreateItemForm
    template_name = 'shop/staff_update_item.html'
    success_url = reverse_lazy('staff_manage_items')


class StaffAddItem(CreateView):
    '''
    Allows a shop staff member to add an item to the shop inventory.
    '''
    model = ShopItems
    form_class = StaffCreateItemForm
    template_name = 'shop/staff_add_item.html'
    success_url = reverse_lazy('shop')


class StaffDeleteItem(DeleteView):
    '''
    Allows a shop staff member to delete a shop item from the inventory.
    '''
    model = ShopItems
    template_name = 'shop/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_manage_items')


class StaffAddImage(CreateView):
    '''
    Allows a staff member to add images to a product.
    '''
    model = ShopItemImage
    form_class = StaffImageUploadForm
    template_name = 'shop/staff_add_image.html'
    success_url = reverse_lazy('staff_manage_items')
