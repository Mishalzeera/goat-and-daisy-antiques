from django import forms
from .models import Customer, StaffMember
from django.contrib.auth.forms import UserCreationForm


class UserAuthAccountCreationForm(UserCreationForm):
    '''
    Extends the built-in Django User Creation Form, updating the email field
    with some placeholder text.
    '''
    email = forms.EmailField(
        initial=None,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter a unique email address'})
    )


class CustomerSignupForm(forms.ModelForm):
    '''
    A form that allows a new user to signup for an account. The username and email fields were showing the defaults in the live server, so a way was found to replace the placeholder text using a widget. From Stack Overflow.
    '''
    
    class Meta:
        model = Customer
        fields = ['full_name', 'address1', 'address2',
                  'postcode', 'town_or_city', 'country']


class CustomerUpdateForm(forms.ModelForm):
    '''
    A form that allows shop admin staff to update customer information, 
    including the notes field which is kept secret from the client. 
    '''

    class Meta:
        model = Customer
        fields = ['full_name', 'address1', 'address2',
                  'postcode', 'town_or_city', 'country', 'notes']


class StaffMemberRegistrationForm(forms.ModelForm):
    '''
    A form for admin to allow permissions for staff members.
    '''

    full_name = forms.CharField(
        initial=None,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter staff members full name.'})
    )

    class Meta:
        model = StaffMember
        readonly_fields = ['username']
        fields = ['full_name', 'shop_staff', 'workshop_staff',
                  'admin_access_permission', 'notes', 'admin_notes']


class StaffUserManagementForm(forms.ModelForm):
    '''
    This form may be inappropriate - there may be no case use for a member registration other than by the admin, who will set the individual permissions. Placeholders also needed to be interjected, see previous class for more.
    '''

    full_name = forms.CharField(initial=None, widget=forms.TextInput(
        attrs={'placeholder': 'Enter full name'}))

    email = forms.EmailField(
        initial=None,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter a unique email address'})
    )

    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'notes']


class AdminStaffManagementForm(forms.ModelForm):
    '''
    The boss's main portal to entering in a new employee and manage employee 
    permissions. 
    '''

    full_name = forms.CharField(initial=None, widget=forms.TextInput(
        attrs={'placeholder': 'Enter full name'}))

    email = forms.EmailField(
        initial=None,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter a unique email address'})
    )

    class Meta:
        model = StaffMember
        exclude = ["user_auth_account"]
