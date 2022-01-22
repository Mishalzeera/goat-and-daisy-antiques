from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView
from django.views.generic.detail import DetailView
from profiles.models import Customer, StaffMember
from .models import ServiceTicket, TicketImage
from .forms import CustomerCreateServiceTicketForm, CustomerUploadImageForm


class Workshop(View):
    '''
    A view that returns the workshop area, where customers can see the kind of 
    work that G&D has done, log in or create an account. If a customer is logged in, there is an option to view their Customer Workbench.
    '''

    def get(self, request, *args, **kwargs):
        return render(request, 'repairs_restorals/workshop.html')


def create_service_ticket(request):

    if request.method == 'GET':
        form = CustomerCreateServiceTicketForm()

        context = {
            'form': form,
        }

        return render(request, 'repairs_restorals/create_service_ticket.html', context)

    if request.method == 'POST':

        customer = get_object_or_404(Customer, username=request.user)

        if customer.has_active_repairs == False:
            customer.has_active_repairs = True
            customer.save()

        form = CustomerCreateServiceTicketForm(request.POST)

        form.instance.customer = customer
        form.instance.workshop_staff_responsible = StaffMember.objects.get(
            pk=8)

        if form.is_valid:
            form.save()

        return render(request, 'repairs_restorals/workshop.html')


def customer_add_image(request):

    if request.method == 'GET':
        '''
        The GET method must return an image upload form with two fields. One 
        field is a list of request.users tickets. Once a ticket is selected, 
        the user can upload an image which will be linked to that ticket.
        '''

        form = CustomerUploadImageForm()
        customer = get_object_or_404(Customer, username=request.user)
        form.fields['service_ticket'].queryset = ServiceTicket.objects.filter(
            customer=customer)
        context = {
            'form': form,
        }
        return render(request, 'repairs_restorals/add_image.html', context)

    if request.method == 'POST':
        return render(request, 'repairs_restorals/add_image.html')


class CustomerWorkbench(ListView):
    ''' 
    A view that displays the Customers current Service Tickets, previous completed projects. 
    '''
    model = ServiceTicket
    template_name = 'repairs_restorals/customer_workbench.html'
    context_object_name = 'tickets'

    def get_context_data(self, **kwargs):
        customer = get_object_or_404(Customer, username=self.request.user)
        # You have to create an empty dictionary first, then add iterable
        # context objects
        context = dict()
        context['tickets'] = ServiceTicket.objects.filter(customer=customer)
        return context
