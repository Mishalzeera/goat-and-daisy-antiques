from django.forms import ModelForm
from django import forms
from .models import ServiceTicket, TicketImage


class CustomerCreateServiceTicketForm(ModelForm):

    class Meta:
        model = ServiceTicket
        fields = ['title', 'service_description', 'link_to_desired_materials_1',
                  'link_to_desired_materials_2', 'link_to_desired_materials_3', ]


class CustomerUploadImageForm(ModelForm):
    class Meta:
        model = TicketImage
        fields = ['service_ticket', 'image']
