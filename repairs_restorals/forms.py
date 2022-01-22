from django.forms import ModelForm
from django import forms
from .models import ServiceTicket, TicketImage


class CustomerCreateServiceTicketForm(ModelForm):
    link_to_desired_materials_1 = forms.URLField(required=False,
                                                 help_text="Please include http://www or https://www in your links.")
    link_to_desired_materials_2 = forms.URLField(required=False,
                                                 help_text="Please include http://www or https://www in your links.")
    link_to_desired_materials_3 = forms.URLField(required=False,
                                                 help_text="Please include http://www or https://www in your links.")

    class Meta:
        model = ServiceTicket
        fields = ['title', 'service_description', 'link_to_desired_materials_1',
                  'link_to_desired_materials_2', 'link_to_desired_materials_3', ]


class CustomerUploadImageForm(ModelForm):

    # def __init__(self, request, *args, **kwargs):
    #     # Since access to the request user is required, the init method
    #     # has to be overriden
    #     super(CustomerUploadImageForm, self).__init__(*args, **kwargs)
    #     # Now set the queryset...
    #     self.fields['service_ticket'].queryset = ServiceTicket.objects.filter(customer=request.user)

    # service_ticket = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = TicketImage
        fields = ['service_ticket', 'image']
