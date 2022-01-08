from django.db import models
from django.contrib.auth.models import User 


class Customer(models.Model):
    ''' 
    Any account created is basically an instance of this model with a one to one relationship with a User in the built in Django auth. 

    '''
    user_auth_account = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=40, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    has_active_shop_orders = models.BooleanField(default=False)
    has_active_repairs = models.BooleanField(default=False)



class StaffMember(models.Model):
    '''
    Every member of staff can be described by this model, which determines their permissions within the custom CMS interfaces.

    '''

    user_auth_account = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    shop_staff = models.BooleanField(default=False)
    workshop_staff = models.BooleanField(default=False)
    overlord_permission = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

