from django import forms
from django.shortcuts import get_object_or_404
from invoices.models import WorkshopCustomerInvoice
from profiles.models import Customer
from .models import ServiceTicket, TicketImage, TodoList, TodoItem


class CustomerCreateServiceTicketForm(forms.ModelForm):
    '''
    Form allowing an authenticated customer user to create a service ticket,
    entering their own titles, descriptions, links
    '''
    # The url fields dont give any formatting hints, so help text was needed.
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


class CustomerUpdateTicketForm(forms.ModelForm):
    '''
    Form allowing an authenticated customer user to create a service ticket,
    entering their own titles, descriptions, links
    '''
    # The url fields dont give any formatting hints, so help text was needed.
    link_to_desired_materials_1 = forms.URLField(required=False,
                                                 help_text="Please include http://www or https://www in your links.")
    link_to_desired_materials_2 = forms.URLField(required=False,
                                                 help_text="Please include http://www or https://www in your links.")
    link_to_desired_materials_3 = forms.URLField(required=False,
                                                 help_text="Please include http://www or https://www in your links.")

    class Meta:
        model = ServiceTicket
        fields = ['link_to_desired_materials_1',
                  'link_to_desired_materials_2', 'link_to_desired_materials_3', ]


class CustomerUploadImageForm(forms.ModelForm):
    '''
    Form that allows a customer to upload an example image - customer selects
    from a list of current projects (a queryset sent from views.customer_add_
    image) and then upload a linked image
    '''

    def __init__(self, *args, **kwargs):

        # Ensures only the service tickets belonging to the current user are
        # displayed as options in the form dropdown box

        self.request = kwargs.pop('request')
        super(CustomerUploadImageForm, self).__init__(*args, **kwargs)
        customer = get_object_or_404(Customer, username=self.request.user)
        self.fields['service_ticket'].queryset = ServiceTicket.objects.filter(
            customer=customer).filter(is_completed=False)

    class Meta:
        model = TicketImage
        fields = ['service_ticket', 'image']

class CustomerInvoiceUpdateForm(forms.ModelForm):
    class Meta:
        model = WorkshopCustomerInvoice
        fields = '__all__'

    
class CreateTodoListForm(forms.ModelForm):
    '''
    A form to create a Todo List.
    '''
    class Meta:
        model = TodoList
        fields = ['subject']


class CreateTodoListItemForm(forms.ModelForm):
    '''
    A form to create Todo List Items.
    '''
    class Meta:
        model = TodoItem
        fields = ['title', 'is_completed']
