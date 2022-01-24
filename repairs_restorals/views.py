from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
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
    '''
    Allows an authenticated user to create a service ticket. If a user isn't
    authenticated, they are given links to login or register.
    '''

    if request.method == 'GET':
        # The GET method creates a simple empty form

        form = CustomerCreateServiceTicketForm()

        context = {
            'form': form,
        }

        return render(request, 'repairs_restorals/create_service_ticket.html', context)

    if request.method == 'POST':
        # The POST method gets the customer using the request object
        customer = get_object_or_404(Customer, username=request.user)

        # ...checking the has_active_repairs Boolean and updating it
        if customer.has_active_repairs == False:
            customer.has_active_repairs = True
            customer.save()

        # An form with the POST data is instantiated
        form = CustomerCreateServiceTicketForm(request.POST)

        # The customer field, which isn't displayed on the template, is
        # assigned here
        form.instance.customer = customer

        # The Workshop Staff field, which is a fixed constant, is added here
        #  to be updated as necessary in the admin panel
        form.instance.workshop_staff_responsible = StaffMember.objects.get(
            pk=8)

        #  The form validity is checked and saved
        if form.is_valid:
            form.save()

        return render(request, 'repairs_restorals/workshop.html')


# def customer_add_image(request):

#     if request.method == 'GET':
#         '''
#         The GET method must return an image upload form with two fields. One
#         field is a list of request.users tickets. Once a ticket is selected,
#         the user can upload an image which will be linked to that ticket
#         '''

#         form = CustomerUploadImageForm()
#         customer = get_object_or_404(Customer, username=request.user)
#         form.fields['service_ticket'].queryset = ServiceTicket.objects.filter(
#             customer=customer)
#         context = {
#             'form': form,
#         }
#         return render(request, 'repairs_restorals/add_image.html', context)

#     if request.method == 'POST':
#         '''The POST method creates an instance of a TicketImage via the
#         upload form and saves it'''

#         form = CustomerUploadImageForm(request.POST, request.FILES)

#         if form.is_valid:
#             form.save()

#         return render(request, 'repairs_restorals/add_image.html')

class CustomerAddImage(CreateView):
    '''
    Allows a customer to add images to service tickets.
    '''
    model = TicketImage
    form_class = CustomerUploadImageForm
    template_name = 'repairs_restorals/add_image.html'
    success_url = reverse_lazy('workshop')

    def get_form_kwargs(self):
        """ 
        Passes the request object to the form class.
        This is necessary to only display tickets that belong to a given 
        user.
        """

        kwargs = super(CustomerAddImage, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CustomerWorkbench(ListView):
    ''' 
    A view that displays the Customers current Service Tickets, previous completed projects. 
    '''
    model = ServiceTicket
    template_name = 'repairs_restorals/customer_workbench.html'
    context_object_name = 'tickets'

    def get_context_data(self, **kwargs):
        # 'customer' is gotten via the request object
        customer = get_object_or_404(Customer, username=self.request.user)

        # Create an empty dictionary first...
        context = dict()

        # ...then add iterable context objects
        context['tickets'] = ServiceTicket.objects.filter(customer=customer)

        return context


class ServiceTicketDetail(DetailView):
    '''
    Allows a customer to view a specific service ticket.
    '''
    model = ServiceTicket
    template_name = 'repairs_restorals/service_ticket.html'
    context_object_name = 'ticket'


class ServiceTicketUpdate(UpdateView):
    '''
    Allows a user to update a current service ticket, most fields restricted
    so that any fundamental changes to a project will have to involve a staff
    member.
    '''
    model = ServiceTicket
    fields = ['title', 'service_description', 'link_to_desired_materials_1',
              'link_to_desired_materials_2', 'link_to_desired_materials_3']
    template_name = 'repairs_restorals/update_service_ticket.html'
    success_url = reverse_lazy('workshop')


class WorkshopStaffTicketOverview(ListView):
    '''
    Allows workshop staff to view all current tickets, with CRUD options.
    '''
 
    queryset = Customer.objects.prefetch_related(
        'service_ticket').filter(has_active_repairs=True)
    template_name = 'repairs_restorals/workshop_ticket_overview.html'
    context_object_name = 'customers'


class TicketDelete(DeleteView):
    '''
    Allows workshop staff to delete a ticket.
    '''
    model = ServiceTicket
    template_name = 'repairs_restorals/ticket_confirm_delete.html'
    success_url = reverse_lazy('workshop')
