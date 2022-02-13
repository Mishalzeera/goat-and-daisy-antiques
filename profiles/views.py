from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import View, CreateView, UpdateView, DetailView, ListView
from .forms import AdminStaffManagementForm, CustomerSignupForm, UserAuthAccountCreationForm, StaffMemberRegistrationForm, CustomerUpdateForm, PublicCustomerUpdateForm
from .models import Customer, StaffMember


class LoginAUser(LoginView):
    '''
    A view to customize the login process.
    '''
    pass


class CustomerProfilePage(LoginRequiredMixin, View):
    '''
    Returns a page allowing a user some CRUD functionality over their profiles, as well as modify user settings.
    '''
    login_url = "/profiles/login/"
    def get(self, request, *args, **kwargs):
        profile = User.objects.get(pk=request.user.id)
        customer = Customer.objects.get(username=request.user)
        

        context = {
            'profile': profile,
            'customer': customer,
        }

        return render(request, 'registration/customer_profile.html', context)


class UserSignupPage(View):
    '''
    Returns an auth account signup page using a form which extends the built-in
    Django user creation form. See forms.py in this module.
    '''

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


class CreateProfilePage(CreateView):
    '''
    Creates a users profile containing specifics not related to authentication.
    '''
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


class StaffMemberSignupPage(View):
    '''
    Returns an auth account signup page using a form which extends the built-in
    Django user creation form. 
    '''

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


class CreateStaffProfilePage(CreateView):
    '''
    Extends the built in CreateView model, creates staff profile containing specifics not related to authentication.
    '''
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


class AdminStaffList(ListView):
    '''
    This view allows the admin to manage all users in the database.
    '''
    queryset = StaffMember.objects.all()
    template_name = 'registration/all_staff.html'
    context_object_name = 'members'


class AllShopCustomers(ListView):
    queryset = Customer.objects.filter(has_active_shop_orders=True)
    template_name = 'shop/all_customers.html'
    context_object_name = 'customers'


class AdminStaffUpdate(UpdateView):
    '''
    This view allows the admin to set broad permissions for staff members.
    '''
    model = StaffMember
    form_class = StaffMemberRegistrationForm
    context_object_name = 'staff_member'
    template_name = "registration/admin_staff_update.html"


class CustomerAccountUpdate(UpdateView):
    '''
    This view allows staff to modify customer accounts.
    '''
    model = Customer
    form_class = CustomerUpdateForm
    context_object_name = 'customer'
    template_name = "registration/customer_account_update.html"


class PublicCustomerAccountUpdate(LoginRequiredMixin, UpdateView):
    '''
    This view allows customer to modify customer accounts.
    '''
    login_url = "/profiles/login/"
    model = Customer
    form_class = PublicCustomerUpdateForm
    context_object_name = 'customer'
    template_name = "registration/customer_account_update.html"


class AdminOverview(View):
    '''
    Returns a superuser overview page, ensures that the employee enrollment
    process is correctly handled - also handy access to employee permissions 
    '''

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/admin_overview.html')


class StaffMemberDetailView(DetailView):
    '''
    Returns a superuser-only detail view of staff members
    '''
    model = StaffMember
    template_name = 'registration/staff_member.html'
    context_object_name = 'member'
