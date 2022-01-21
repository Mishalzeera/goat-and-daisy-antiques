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
    class Meta:
        model = TicketImage
        fields = ['service_ticket', 'image']
