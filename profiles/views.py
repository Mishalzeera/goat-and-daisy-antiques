from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.group_mixin_decorator import GroupRequiredMixin, group_required_decorator
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.views.generic import View, CreateView, UpdateView, DetailView, ListView
from .forms import AdminStaffManagementForm, CustomerSignupForm, UserAuthAccountCreationForm, StaffMemberRegistrationForm, CustomerUpdateForm, PublicCustomerUpdateForm
from .models import Customer, StaffMember
from invoices.models import ShopCustomerInvoice
from repairs_restorals.models import ServiceTicket

# public
class LoginAUser(LoginView):
    """
    A view to customize the login process if needed.
    """

            
# login required
class CustomerProfilePage(LoginRequiredMixin, View):
    """
    Returns a page allowing a user some CRUD functionality over their profiles, as well as modify user settings.
    """
    login_url = "/profiles/login/"

    

    def get(self, request, *args, **kwargs):
        
        profile = get_object_or_404(User, pk=request.user.id)
        try:
            customer = Customer.objects.get(username=request.user)
        except Customer.DoesNotExist:
                customer = StaffMember.objects.get(username=request.user)
        shop_invoices = None
        shop_invoices = ShopCustomerInvoice.objects.filter(email=customer.email)
        workshop_tickets = ServiceTicket.objects.filter(customer_id=customer.id)
        

        context = {
            'profile': profile,
            'customer': customer,
            'shop_invoices': shop_invoices,
            'workshop_tickets': workshop_tickets
        }

        return render(request, 'registration/customer_profile.html', context)


# login required
class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    """
    Allows a user to change their password.
    """
    success_url = reverse_lazy('password_changed')

# redirect page
def password_changed(request):
    """
    Displays a success message when password is changed.
    """
    return render(request, 'registration/password_changed.html')

# public
class UserSignupPage(View):
    """
    Returns an auth account signup page using a form which extends the built-in
    Django user creation form. See forms.py in this module.
    """

    def get(self, request, *args, **kwargs):
        # Send an instance of the account creation form to the template
        form = UserAuthAccountCreationForm()

        context = {
            "form": form,
        }

        return render(request, 'registration/signup.html', context)

    def post(self, request, *args, **kwargs):
        # Get the new account details from the request object
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']

        # ...use them to create a new user and save
        newuser = User.objects.create_user(username, email, password)
        newuser.save()
        # Explicitly log in the user
        login(request, newuser)
        # Then redirect to the create profile view
        return redirect('create_profile')


# public
class CreateProfilePage(CreateView):
    """
    Creates a users profile containing specifics not related to authentication.
    """
    model = Customer
    template_name = "registration/create_customer_profile.html"
    fields = ['full_name', 'address1', 'address2',
              'postcode', 'town_or_city', 'country', 'notes']

    def form_valid(self, form):
        # this method is to ensure that 1. the username used to create the
        # auth account is automatically added to the new profile, linking the
        # two in a one-to-one relationship. No chance for the user to make
        # a mess by using a different username at this point in the process.
        # 2. the same email address is used as well, which requires
        # a different process than the username.
        form.instance.username = self.request.user
        user = User.objects.get(username=self.request.user)
        form.instance.email = user.email
        return super().form_valid(form)


# admin only
class StaffMemberSignupPage(GroupRequiredMixin, View):
    """
    Returns an auth account signup page using a form which extends the built-in
    Django user creation form. 
    """
    group_required = [u'Admin Only']
    def get(self, request, *args, **kwargs):
        # Send a blank form to the template
        form = UserAuthAccountCreationForm()

        context = {
            "form": form,
        }
        return render(request, 'registration/staff_auth_signup.html', context)

    def post(self, request, *args, **kwargs):
        # Get the new account details from the request object, use them to
        # create a new user.
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']

        # The username value is passed into a session cookie
        # which allows the admin to create the linked staff member profile
        # page (next view)
        request.session['username_cookie'] = username

        # New user is created and saved
        newuser = User.objects.create_user(username, email, password)
        newuser.save()
        # Then redirect to the create staff profile view
        return redirect('create_staff_profile')


# admin only
class CreateStaffProfilePage(GroupRequiredMixin, CreateView):
    """
    Extends the built in CreateView model, creates staff profile containing specifics not related to authentication.
    """
    group_required = [u'Admin Only']
    model = StaffMember
    form_class = StaffMemberRegistrationForm
    template_name = "registration/create_staff_profile.html"

    def form_valid(self, form):
        # this method is to ensure that 1. the username used to create the
        # auth account is automatically added to the new profile, linking the
        # two in a one-to-one relationship. No chance for the admin to make
        # a mess by using the wrong username at this point in the process.
        # 2. this time the session cookie is used as to filter the
        # objects.get() method.
        user = User.objects.get(
            username=self.request.session['username_cookie'])

        # The form instance is assigned the correct values
        form.instance.username = user
        form.instance.email = user.email
        return super().form_valid(form)


# admin only
class AdminStaffList(GroupRequiredMixin, ListView):
    """
    This view allows the admin to manage all staff in the database.
    """
    group_required = [u'Admin Only']
    queryset = StaffMember.objects.all()
    template_name = 'registration/all_staff.html'
    context_object_name = 'members'


# general staff
class AllShopCustomers(GroupRequiredMixin, ListView):
    """
    Lists all the customers registered in the system.
    """
    group_required = [u'General Staff']
    queryset = Customer.objects.all()
    template_name = 'shop/all_customers.html'
    context_object_name = 'customers'


# admin only
class AdminStaffUpdate(GroupRequiredMixin, UpdateView):
    """
    This view allows the admin to manage staff members.
    """
    group_required = [u'Admin Only']
    model = StaffMember
    form_class = StaffMemberRegistrationForm
    context_object_name = 'staff_member'
    template_name = "registration/admin_staff_update.html"


# general staff
class CustomerAccountUpdate(GroupRequiredMixin, UpdateView):
    """
    This view allows staff to modify customer accounts.
    """
    group_required = [u'General Staff']
    model = Customer
    form_class = CustomerUpdateForm
    context_object_name = 'customer'
    template_name = "registration/customer_account_update.html"


# login required
class PublicCustomerAccountUpdate(LoginRequiredMixin, UpdateView):
    """
    This view allows customer to modify customer accounts.
    """
    login_url = "/profiles/login/"
    model = Customer
    form_class = PublicCustomerUpdateForm
    context_object_name = 'customer'
    template_name = "registration/customer_account_update.html"


# admin only
class AdminOverview(GroupRequiredMixin, View):
    """
    Returns a superuser overview page, ensures that the employee enrollment
    process is correctly handled - also handy access to employee permissions 
    """
    group_required = [u'Admin Only']

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/admin_overview.html')


# admin only
class StaffMemberDetailView(GroupRequiredMixin, DetailView):
    """
    Returns a superuser-only detail view of staff members
    """
    group_required = [u'Admin Only']
    model = StaffMember
    template_name = 'registration/staff_member.html'
    context_object_name = 'member'
