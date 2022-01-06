from django.shortcuts import render
from django.views.generic import View, ListView
from django.views.generic.detail import DetailView




class Workshop(View):
    '''
    A view that returns the workshop area, where customers can see the kind of 
    work that G&D has done, log in or create an account. If a customer is logged in, there is an option to view their Customer Workbench.
    '''

    def get(self, request, *args, **kwargs):
        return render(request, 'repairs_restorals/workshop.html')


class CustomerWorkbench(ListView):
    ''' 
    A view that displays the Customers current Service Tickets, previous completed projects. 
    '''
    pass


class ServiceTicket(DetailView):
    '''
    A view that allows the Customer to see a current Service Ticket, create/edit/delete a Service Ticket
    '''
    pass


