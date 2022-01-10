from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import View
from .forms import AdminStaffManagementForm, CustomerSignupForm


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

        form = CustomerSignupForm()

        context = {
            "form": form,
        }

        return render(request, 'registration/signup.html', context)

    
    def post(self, request, *args, **kwargs):

        messages.success(request, ("POST REQUEST MADE"))

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