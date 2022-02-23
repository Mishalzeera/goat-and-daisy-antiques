from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from profiles.group_mixin_decorator import GroupRequiredMixin, group_required_decorator
from django.views.generic.detail import DetailView
from invoices.models import WorkshopCustomerInvoice
from profiles.models import Customer, StaffMember
from .models import ServiceTicket, TicketImage, TodoList, TodoItem
from .forms import CustomerCreateServiceTicketForm, CustomerUploadImageForm, CustomerUpdateTicketForm, StaffCustomerInvoiceUpdateForm, CreateTodoListForm, CreateTodoListItemForm, AdminCreateTodoListForm


# public
class Workshop(View):
    """
    A view that returns the workshop area, where customers can see the kind of 
    work that G&D has done, log in or create an account. If a customer is logged in, there is an option to view their Customer Workbench.
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'repairs_restorals/workshop.html')


# login required
@login_required
def create_service_ticket(request):
    """
    Allows an authenticated user to create a service ticket. If a user isn't
    authenticated, they are given links to login or register.
    """

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

        # A form with the POST data is instantiated
        form = CustomerCreateServiceTicketForm(request.POST)

        # The customer field, which isn't displayed on the template, is
        # assigned here
        form.instance.customer = customer

        # The Workshop Staff field, which is set by admin, is added here

        form.instance.workshop_staff_responsible = StaffMember.objects.get(
            default_workshop_staff=True)

        #  The form validity is checked and saved
        if form.is_valid:
            form.save()

        # An alert is shown to the customer
        messages.success(
            request, ("Service Ticket successfully created! Please check your inbox for confirmation email."))

        return render(request, 'repairs_restorals/workshop.html')


# login required
class CustomerAddImage(LoginRequiredMixin, CreateView):
    """
    Allows a customer to add images to service tickets.
    """
    login_url = '/profiles/login/'
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


# login required
class CustomerWorkbench(LoginRequiredMixin, ListView):
    """ 
    A view that displays the Customers current Service Tickets, previous completed projects. 
    """
    login_url = '/profiles/login/'
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


# login required
class ServiceTicketDetail(LoginRequiredMixin, DetailView):
    """
    Allows a customer to view a specific service ticket.
    """
    login_url = '/profiles/login/'
    model = ServiceTicket
    template_name = 'repairs_restorals/service_ticket.html'
    context_object_name = 'ticket'


# workshop staff only
class ServiceTicketUpdate(GroupRequiredMixin, UpdateView):
    """
    Allows staff to update a current service ticket.
    """
    group_required = [u'Workshop Staff']

    model = ServiceTicket
    fields = ['title', 'service_description', 'link_to_desired_materials_1',
              'link_to_desired_materials_2', 'link_to_desired_materials_3', 'is_completed']
    template_name = 'repairs_restorals/update_service_ticket.html'
    success_url = reverse_lazy('ticket_overview')


# login required
class PublicServiceTicketUpdate(LoginRequiredMixin, UpdateView):
    """
    Allows a customer to update a current service ticket, most fields restricted
    so that any fundamental changes to a project will have to involve a staff
    member.
    """
    login_url = '/profiles/login/'
    model = ServiceTicket
    form_class = CustomerUpdateTicketForm
    context_object_name = "customer_ticket"
    template_name = 'repairs_restorals/update_service_ticket.html'
    success_url = reverse_lazy('workshop')


# workshop staff only
class WorkshopStaffTicketOverview(GroupRequiredMixin, ListView):
    """
    Allows workshop staff to view all current tickets, with CRUD options.
    """
    group_required = [u'Workshop Staff']
    queryset = Customer.objects.prefetch_related(
        'service_ticket').filter(has_active_repairs=True)
    template_name = 'repairs_restorals/workshop_ticket_overview.html'
    context_object_name = 'customers'


# workshop staff only
class TicketDelete(GroupRequiredMixin, DeleteView):
    """
    Allows workshop staff to delete a ticket.
    """
    group_required = [u'Workshop Staff']
    model = ServiceTicket
    template_name = 'repairs_restorals/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket_overview')


# workshop staff only
class WorkshopStaffUpdateImage(GroupRequiredMixin, UpdateView):
    """
    Allows a workshop staff member to update a specific image.
    """
    group_required = [u'Workshop Staff']
    model = TicketImage
    form_class = CustomerUploadImageForm
    template_name = 'repairs_restorals/update_image.html'
    success_url = reverse_lazy('ticket_overview')


# workshop staff only
class WorkshopStaffDeleteImage(GroupRequiredMixin, DeleteView):
    """
    Allows a workshop staff member to delete ticket images.
    """

    group_required = [u'Workshop Staff']
    model = TicketImage
    template_name = 'shop/staff_confirm_delete.html'
    success_url = reverse_lazy('ticket_overview')


# general staff - would be good to make it its own app
class TaskManager(GroupRequiredMixin, View):
    """
    Shows a list of todo items for each workshop staff member, allowing
    all CRUD functions on the same page for convenience. 
    """
    group_required = [u'General Staff']

    def get(self, request, *args, **kwargs):
        # Get a staff member
        staff_member = get_object_or_404(
            StaffMember, username=self.request.user)

        # Get a todo list filtered by staff member
        todo_list = TodoList.objects.prefetch_related(
            'items').filter(staff_member=staff_member)

        # Create a todo list form
        todo_list_form = CreateTodoListForm()

        # Create a todo list item form
        todo_list_item_form = CreateTodoListItemForm()

        # Put them in the context
        context = {
            'todo_list': todo_list,
            'todo_list_form': todo_list_form,
            'todo_list_item_form': todo_list_item_form,

        }

        # Send them to the template
        return render(request, 'repairs_restorals/todo_list.html', context)

    def post(self, request, *args, **kwargs):
        # Awkward but it works

        # Create a list form for refreshed page
        todo_list_form_instance = CreateTodoListForm(request.POST)

        # Get the staff member by the request object
        staff_member = get_object_or_404(
            StaffMember, username=self.request.user)

        # Assign the staff member to the instance of the form
        todo_list_form_instance.instance.staff_member = staff_member

        # Check validity and save
        if todo_list_form_instance.is_valid():
            todo_list_form_instance.save()

        # If there is a custom name sent from the template
        if 'todo_list_item' in request.POST:

            # The instance is intialised from the POST data (custom form in
            # template - its not a model form instance, in order to be
            # able to use the List id in the for loop. In the template.)
            todo_item_form_instance = CreateTodoListItemForm(request.POST)

            # The foreign key relationship is set for the unique instance,
            # so that list items and lists are coherently linked
            related_todo = TodoList.objects.get(
                pk=request.POST['todo_list_item'])
            todo_item_form_instance.instance.todo_list_id = related_todo.id

            # The todo list item is validated and saved
            if todo_item_form_instance.is_valid():
                todo_item_form_instance.save()

        return redirect('task_manager')


# admin only
class AdminTaskCreate(GroupRequiredMixin, View):
    """
    Shows a list of todo items for each workshop staff member, allowing
    all CRUD functions on the same page for convenience. 
    """
    group_required = [u'Admin Only']

    def get(self, request, *args, **kwargs):
        todo_lists = TodoList.objects.filter(
            admin_created=True).order_by('staff_member')

        # Create a todo list form
        todo_list_form = AdminCreateTodoListForm()

        # Create a todo list item form
        todo_list_item_form = CreateTodoListItemForm()

        # Put them in the context
        context = {
            'todo_list': todo_lists,
            'todo_list_form': todo_list_form,
            'todo_list_item_form': todo_list_item_form,

        }

        # Send them to the template
        return render(request, 'repairs_restorals/admin_todo_list.html', context)

    def post(self, request, *args, **kwargs):

        # Create a list form for refreshed page
        todo_list_form_instance = AdminCreateTodoListForm(request.POST)
        todo_list_form_instance.instance.admin_created = True

        # Check validity and save
        if todo_list_form_instance.is_valid():
            todo_list_form_instance.save()

        # If there is a custom name sent from the template
        if 'todo_list_item' in request.POST:

            # The instance is intialised from the POST data (custom form in
            # template - its not a model form instance, in order to be
            # able to use the List id in the for loop. In the template.)
            todo_item_form_instance = CreateTodoListItemForm(request.POST)

            # The foreign key relationship is set for the unique instance,
            # so that list items and lists are coherently linked
            related_todo = TodoList.objects.get(
                pk=request.POST['todo_list_item'])
            todo_item_form_instance.instance.todo_list_id = related_todo.id

            # The todo list item is validated and saved
            if todo_item_form_instance.is_valid():
                todo_item_form_instance.save()

        return redirect('admin_task_manager')


# Admin only
class AdminTaskManagerOverview(GroupRequiredMixin, ListView):
    """
    Gives Admin a way to keep an eye on what everyone is up to. Big brother is
    watching you. 
    """
    # model = TodoList
    group_required = [u'Admin Only']
    template_name = 'repairs_restorals/admin_task_manager.html'
    queryset = TodoList.objects.prefetch_related(
        "items").all().order_by('staff_member')
    context_object_name = 'todo_lists'


# general staff
@group_required_decorator('General Staff')
def delete_or_update_item_in_todo(request, pk):
    """
    A function that allows a list item to be deleted in the 
    workshop todo list app, bypassing "are you sure" stage.
    """
    # Get the item by the pk sent from the template and delete
    if 'delete_list_item' in request.GET:
        item = TodoItem.objects.get(pk=pk)
        item.delete()

    # Get the list by the pk sent from the template and delete
    if 'delete_list' in request.GET:

        item = TodoList.objects.get(pk=pk)
        item.delete()

    # Get the list item by the pk from the template and toggle
    if 'toggle_item' in request.GET:

        item = TodoItem.objects.get(pk=pk)

        # Toggle the is_completed status
        if item.is_completed == False:
            item.is_completed = True
        elif item.is_completed:
            item.is_completed = False

        item.save()

    # Get the staff member by the request object

    return redirect('task_manager')


# admin only
@group_required_decorator('Admin Only')
def admin_delete_or_update_item_in_todo(request, pk):
    """
    A function that allows a list item to be deleted in the 
    admin todo list app, bypassing "are you sure" stage.
    """
    # Get the item by the pk sent from the template and delete
    if 'delete_list_item' in request.GET:
        item = TodoItem.objects.get(pk=pk)
        item.delete()

    # Get the list by the pk sent from the template and delete
    if 'delete_list' in request.GET:

        item = TodoList.objects.get(pk=pk)
        item.delete()

    # Get the list item by the pk from the template and toggle
    if 'toggle_item' in request.GET:

        item = TodoItem.objects.get(pk=pk)

        # Toggle the is_completed status
        if item.is_completed == False:
            item.is_completed = True
        elif item.is_completed:
            item.is_completed = False

        item.save()

    # The todo list is fetched again, filtered by admin_created
    # todo_list = TodoList.objects.filter(
    #     admin_created=True).order_by('staff_member')

    # New forms are sent
    # todo_list_form = AdminCreateTodoListForm({'admin_created': True})
    # todo_list_item_form = CreateTodoListItemForm()

    # Context is filled in again
    # context = {
    #     'todo_list': todo_list,
    #     'todo_list_form': todo_list_form,
    #     'todo_list_item_form': todo_list_item_form,

    # }

    # ...and sent to the template
    return redirect('admin_task_manager')


# login required
class PublicCustomerInvoices(LoginRequiredMixin, ListView):
    """
    Customer can view his or her own invoices.
    """
    login_url = '/profiles/login/'
    model = WorkshopCustomerInvoice
    context_object_name = 'invoices'
    template_name = 'repairs_restorals/customer_invoices.html'

    def get_context_data(self, **kwargs):
        # 'customer' is gotten via the request object
        customer = get_object_or_404(Customer, username=self.request.user)

        # Create an empty dictionary first...
        context = {}

        # ...then add iterable context objects
        context['invoices'] = WorkshopCustomerInvoice.objects.filter(
            service_ticket__customer_id=customer.id)

        return context


# workshop staff only
class AllCustomerInvoices(GroupRequiredMixin, ListView):
    """
    Shows workshop staff all the invoices in the system.
    """
    group_required = [u'Workshop Staff']
    model = WorkshopCustomerInvoice
    template_name = 'repairs_restorals/all_customer_invoices.html'
    context_object_name = "invoices"


# workshop staff only
class AdminCustomerDetailView(GroupRequiredMixin, DetailView):
    """
    Allows a workshop staff member to see details of an invoice.
    """
    group_required = [u'Workshop Staff']
    model = WorkshopCustomerInvoice
    template_name = 'repairs_restorals/customer_invoice_detail.html'
    context_object_name = 'invoice'


# workshop staff only
class AdminCustomerInvoice(GroupRequiredMixin, UpdateView):
    """
    Allows a workshop staff member to update a specific invoice.
    """
    group_required = [u'Workshop Staff']
    model = WorkshopCustomerInvoice
    form_class = StaffCustomerInvoiceUpdateForm
    template_name = 'repairs_restorals/admin_customer_invoice.html'
    success_url = reverse_lazy('all_customer_invoices')


# workshop staff only
class WorkshopStaffDeleteInvoice(GroupRequiredMixin, DeleteView):
    """
    Allows a workshop staff member to delete ticket images.
    """

    group_required = [u'Workshop Staff']
    model = WorkshopCustomerInvoice
    template_name = 'shop/staff_confirm_delete.html'
    success_url = reverse_lazy('all_customer_invoices')
