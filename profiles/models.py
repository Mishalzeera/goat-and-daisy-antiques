from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Customer(models.Model):
    """ 
    Any  customer account created is basically an instance of this model with a one to one relationship with a User in the built in Django auth. 
    """
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, editable=False)
    email = models.EmailField(unique=True, default="start@domain.dj")
    full_name = models.CharField(max_length=100, null=True, blank=True)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=40, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    country = models.CharField(max_length=40, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    staff_notes = models.TextField(null=True, blank=True)
    has_active_shop_orders = models.BooleanField(default=False)
    has_active_repairs = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.username)

    def get_absolute_url(self):
        return reverse('index')


class StaffMember(models.Model):
    """
    Every member of staff can be described by this model, which determines their permissions within the custom CMS interfaces. 
    """

    username = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, editable=False)
    email = models.EmailField(unique=True, default="start@domain.dj")
    full_name = models.CharField(max_length=100, default="startname")
    shop_staff = models.BooleanField(default=False)
    workshop_staff = models.BooleanField(default=False)
    admin_access_permission = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    admin_notes = models.TextField(null=True, blank=True)
    default_workshop_staff = models.BooleanField(default=False)

# https://stackoverflow.com/questions/1455126/unique-booleanfield-value-in-django

    def save(self, *args, **kwargs):
        if self.default_workshop_staff:
            try:
                temp = StaffMember.objects.get(default_workshop_staff=True)
                if self != temp:
                    temp.default_workshop_staff = False
                    temp.save()
            except StaffMember.DoesNotExist:
                pass
        super(StaffMember, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.username)

    def get_absolute_url(self):
        return reverse('all_staff')
