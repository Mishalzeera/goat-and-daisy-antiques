# https://stackoverflow.com/questions/6288661/adding-a-user-to-a-group-in-django

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from .models import StaffMember


@receiver(post_save, sender=StaffMember)
def put_staff_member_in_group(sender, instance, created, **kwargs):
    """
    When a staff member is saved in the system, the staff member is sorted into
    the correct permissions group programmatically - saving the admin from 
    having to click through potentially too many users in the admin User 
    field.
    """

    # Get the staff member instance to check admin created perms
    staff_member = StaffMember.objects.get(pk=instance.id)
    # Get the related auth account, where group perms are set
    staff_auth = User.objects.get(username=staff_member.username)
    # Get the admin created groups from the Django Group model
    general_staff = Group.objects.get(name='General Staff')
    workshop_staff = Group.objects.get(name="Workshop Staff")
    shop_staff = Group.objects.get(name="Shop Staff")
    admin_only = Group.objects.get(name="Admin Only")

    # Add everyone to General Staff
    general_staff.user_set.add(staff_auth)

    if staff_member.shop_staff:
        shop_staff.user_set.add(staff_auth)

    if staff_member.workshop_staff:
        workshop_staff.user_set.add(staff_auth)

    if staff_member.admin_access_permission:
        admin_only.user_set.add(staff_auth)

    if not staff_member.shop_staff:
        shop_staff.user_set.remove(staff_auth)

    if not staff_member.workshop_staff:
        workshop_staff.user_set.remove(staff_auth)

    if not staff_member.admin_access_permission:
        admin_only.user_set.remove(staff_auth)

    staff_auth.save()
