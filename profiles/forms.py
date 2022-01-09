from django import forms
from .models import Customer, StaffMember


class CustomerSignupForm(forms.ModelForm):

    username = forms.CharField(
        initial=None,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a username'})
    )

    email = forms.EmailField(
        initial=None,
        widget = forms.TextInput(attrs={'placeholder': 'Enter a unique email address'})
    )

    class Meta:
        model = Customer
        fields = ['username', 'email', 'address1', 'address2', 'postcode',]



class StaffMemberRegistrationForm(forms.ModelForm):

    full_name = forms.CharField(initial=None, widget=forms.TextInput(attrs={'placeholder': 'Enter full name'}))

    email = forms.EmailField(
    initial=None,
    widget = forms.TextInput(attrs={'placeholder': 'Enter a unique email address'})
    )

    class Meta:
        model = StaffMember
        fields = ['full_name', 'email','notes']


class AdminStaffManagementForm(forms.ModelForm):

    full_name = forms.CharField(initial=None, widget=forms.TextInput(attrs={'placeholder': 'Enter full name'}))

    email = forms.EmailField(
    initial=None,
    widget = forms.TextInput(attrs={'placeholder': 'Enter a unique email address'})
    )

    class Meta:
        model = StaffMember
        exclude = ["user_auth_account"]
        
