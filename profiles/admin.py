from django.contrib import admin
from .models import Customer, StaffMember


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'has_repairs', 'has_orders']

    def has_repairs(self, customer):
        if customer.has_active_repairs:
            return "Yes"
        return ""

    def has_orders(self, customer):
        if customer.has_active_shop_orders:
            return "Yes"
        return ""


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'has_shop_permission',
                    'has_workshop_permission']

    def has_shop_permission(self, staff_member):
        if staff_member.shop_staff:
            return "Yes"
        return ""

    def has_workshop_permission(self, staff_member):
        if staff_member.workshop_staff:
            return "Yes"
        return ""
