from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import View
from .forms import AdminStaffManagementForm, CustomerSignupForm
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

        form1 = UserCreationForm()
        form2 = CustomerSignupForm()

        context = {
            "form1": form1,
            "form2": form2,

        }

        return render(request, 'registration/signup.html', context)

    
    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        postcode = request.POST['postcode']
        
        user = User.objects.create_user(username, email, password)
        user.save()

        profile = Customer.objects.create({
            'username': user.username,
            'email': email,
            'address1': address1,
            'address2': address2,
            'postcode': postcode,

        })

        # profile.save()

        return render(request, 'site_layout/index.html')
        

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