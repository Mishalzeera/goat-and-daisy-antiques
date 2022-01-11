from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import View, CreateView
from .forms import AdminStaffManagementForm, CustomerSignupForm, UserAuthAccountCreationForm
from .models import Customer


class LoginAUser(LoginView):
    '''
    A view to customize the login process
    '''
    pass


class UserProfilePage(View):
    '''
    Returns a page allowing a user some CRUD functionality over their profiles, as well as modify user settings 
    '''
    def get(self, request, *args, **kwargs):

        return redirect('index')
    


class UserSignupPage(View):

    def get(self, request, *args, **kwargs):

        form = UserAuthAccountCreationForm()

        context = {
            "form": form,

        }

        return render(request, 'registration/signup.html', context)

    
    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        
        newuser = User.objects.create_user(username, email, password)
        newuser.save()
        
        login(request, newuser)

        return redirect('create_profile')
        

class CreateProfilePage(CreateView):
    model = Customer
    # form_class = ... then no 'fields'.. form Class Meta has model, fields
    template_name = "registration/create_customer_profile.html"
    fields = ['full_name', 'address1', 'address2', 'postcode', 'town_or_city', 'country', 'notes']

    def form_valid(self, form):
        print(self.request.user)
        form.instance.username = self.request.user
        return super().form_valid(form)




class AdminUserManagement(View):
    
    def get(self, request, *args, **kwargs):

        form = AdminStaffManagementForm()

        context = {
            'form': form,
        }

        return render(request, 'registration/admin_overview.html', context)


    def post(self, request, *args, **kwargs):

        messages.success(request, ("POSTPOSTPOSTPOST"))

        return redirect('index')