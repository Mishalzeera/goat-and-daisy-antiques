from django.db import models
from django.contrib.auth.models import User 


class Customer(models.Model):
    ''' 
    Any account created is basically an instance of this model with a one to one relationship with a User in the built in Django auth. 

    '''
    user_auth_account = models.OneToOneField(User, on_delete=models.CASCADE, null=True, editable=False, unique=True)
    username = models.CharField(max_length=100, default="startname", unique=True)
    email = models.EmailField(unique=True, default="start@domain.dj")
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=40, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    staff_notes = models.TextField(null=True, blank=True)
    has_active_shop_orders = models.BooleanField(default=False)
    has_active_repairs = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username




class StaffMember(models.Model):
    '''
    Every member of staff can be described by this model, which determines their permissions within the custom CMS interfaces.

    '''

    user_auth_account = models.OneToOneField(User, on_delete=models.CASCADE, null=True, editable=False)
    full_name = models.CharField(max_length=100, default="startname")
    email = models.EmailField(unique=True, default="start@domain.dj")
    shop_staff = models.BooleanField(default=False)
    workshop_staff = models.BooleanField(default=False)
    admin_access_permission = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    admin_notes = models.TextField(null=True, blank=True)


    def __str__(self) -> str:
        return self.full_name

