from django.contrib import admin
from .models import ShopCustomerInvoice, WorkshopCustomerInvoice

# Register your models here.


@admin.register(ShopCustomerInvoice)
class ShopCustomerInvoiceAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'is_completed']
    readonly_fields = ['order_number']


@admin.register(WorkshopCustomerInvoice)
class WorkshopCustomerInvoiceAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'installment_paid', 'is_completed', 'payment_type']
