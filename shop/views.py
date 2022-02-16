from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.mail import send_mail
from profiles.group_mixin_decorator import GroupRequiredMixin, group_required_decorator
from .models import ShopItems, ShopItemImage
from invoices.models import ShopCustomerInvoice
from profiles.models import Customer
from .forms import StaffCreateItemForm, StaffImageUploadForm, StaffImageUploadFormInProduct


# public
class ShopFront(ListView):
    """
    A view to return all the antiques for sale.
    """
    model = ShopItems
    template_name = 'shop/shop.html'
    queryset = ShopItems.objects.prefetch_related('images').all()
    context_object_name = "products"


# general staff only
class AllShopCustomers(GroupRequiredMixin, ListView):
    """
    A view to return all shop customers with active shop orders.
    """
    group_required = [u'General Staff']
    queryset = Customer.objects.all()
    template_name = 'shop/all_customers.html'
    context_object_name = 'customers'


# shop staff only
class AllShopOrders(GroupRequiredMixin, View):
    """
    Allows shop staff to keep an eye on orders needing to be shipped and
    the status of related payments - via a list of all current shop customer 
    invoices. 
    """
    group_required = ['Shop Staff']

    def get(self, request, *args, **kwargs):
        queryset = ShopCustomerInvoice.objects.all()

        context = {
            'invoices': queryset,
        }

        return render(request, 'shop/all_shop_orders.html', context)


# shop staff only
@group_required_decorator('Shop Staff')
def mark_invoice_complete(request, invoice_order_number):
    """
    When shop staff have shipped an item, this functions marks the invoice
    as complete and sends an email to the customer.
    """
    invoice = ShopCustomerInvoice.objects.get(order_number = invoice_order_number)
    invoice.is_completed = True
    invoice.save()

    return redirect('all_shop_orders')


# public
class ShopItem(DetailView):
    """ 
    A view to return a specific item with options to buy.
    """
    model = ShopItems
    template_name = 'shop/product_detail.html'
    context_object_name = 'item'


# shop staff only
class StaffManageItems(GroupRequiredMixin, ListView):
    """
    Allows a shop staff member to have an overview of inventory with
    CRUD functionality.
    """
    group_required = [u'Shop Staff']
    model = ShopItems
    template_name = 'shop/staff_manage_items.html'
    queryset = ShopItems.objects.prefetch_related('images').all()
    context_object_name = "products"
    


# shop staff only
class StaffAddItem(GroupRequiredMixin, CreateView):
    """
    Allows a shop staff member to add an item to the shop inventory.
    """
    group_required = ['Shop Staff']
    model = ShopItems
    form_class = StaffCreateItemForm
    template_name = 'shop/staff_add_item.html'
    success_url = reverse_lazy('staff_manage_items')


# shop staff only
class StaffDeleteItem(GroupRequiredMixin, DeleteView):
    """
    Allows a shop staff member to delete a shop item from the inventory.
    """
    group_required = ['Shop Staff']
    model = ShopItems
    template_name = 'shop/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_manage_items')


# shop staff only
class StaffUpdateItem(GroupRequiredMixin, UpdateView):
    """
    Allows a shop staff member to change a particular inventory item.
    """
    group_required = ['Shop Staff']
    model = ShopItems
    form_class = StaffCreateItemForm
    template_name = 'shop/staff_update_item.html'
    success_url = reverse_lazy('staff_manage_items')


# shop staff only
class StaffAddImage(GroupRequiredMixin, CreateView):
    """
    Allows a staff member to add images to multiple products without leaving the page.
    """
    group_required = ['Shop Staff']
    model = ShopItemImage
    form_class = StaffImageUploadForm
    template_name = 'shop/staff_add_image.html'
    success_url = reverse_lazy('staff_add_image')

    def post(self, request, *args, **kwargs):
        self.object = None
        messages.success(request, ("Image successfully added."))
        return super().post(request, *args, **kwargs)


# shop staff only
@group_required_decorator('Shop Staff')
def add_image_in_product(request, product_id):
    """
    Allows staff to add images to products from product detail instances(list 
    or detail view) - for convenience
    """
    product = ShopItems.objects.get(pk=product_id)

    if request.method == "GET":

        initial = {'product': product}
        form = StaffImageUploadFormInProduct(initial=initial)
        context = {
            'product': product,
            'form': form,
        }
        return render(request, 'shop/add_image_in_product.html', context)
    
    if request.method == "POST":

        form = StaffImageUploadFormInProduct(request.POST, request.FILES)

        form.instance.product = product
        if form.is_valid():
            form.save()
        
        return redirect('staff_manage_items')


# shop staff only
class StaffUpdateImage(GroupRequiredMixin, UpdateView):
    """
    Allows a shop staff member to update a specific image.
    """
    group_required = ['Shop Staff']
    model = ShopItemImage
    form_class = StaffImageUploadForm
    template_name = 'shop/staff_update_image.html'
    success_url = reverse_lazy('staff_manage_items')


# shop staff only
class StaffDeleteImage(GroupRequiredMixin, DeleteView):
    """
    Allows a shop staff member to delete product images.
    """
    group_required = ['Shop Staff']
    model = ShopItemImage
    template_name = 'shop/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_manage_items')


def set_primary_image(request, product_id, image_id, ):
    """
    Defines an image from a product set as the primary image for display 
    purposes.
    """
    image_set = ShopItemImage.objects.filter(product__id=product_id)
    for img in image_set:
        img.is_primary_image = False
        img.save()
    image = ShopItemImage.objects.get(pk=image_id)
    image.is_primary_image = True
    image.save()


    return redirect('staff_manage_items')



    