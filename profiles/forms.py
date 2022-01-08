from django import forms


class CustomerSignupForm(forms.Form):

    full_name = forms.CharField(label="Full Name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    address1 = forms.CharField(label="Address Line 1", max_length=100, required=False)
    address2 = forms.CharField(label="Address Line 2", max_length=100, required=False)
    postcode = forms.CharField(label="Postcode", max_length=40, required=False)


class StaffMemberRegistrationForm(forms.Form):

    full_name = forms.CharField(label="Full Name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)


class OverlordStaffManagementForm(forms.Form):

    shop_staff = forms.BooleanField(label="Shop Staff")
    workshop_staff = forms.BooleanField(label="Workshop Staff")
    overlord_permission = forms.BooleanField(label="Overlord Permission")
    notes = forms.CharField(label="Notes")
