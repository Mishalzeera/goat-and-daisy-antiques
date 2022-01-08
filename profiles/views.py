from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import View
from .forms import CustomerSignupForm, StaffMemberRegistrationForm, OverlordStaffManagementForm


class LoginUser(LoginView):

    def get(self, request, *args, **kwargs):
        messages.success(request, ("Login User"))
        pass

class UserProfilePage(View):
    '''
    Returns a page allowing a user some CRUD functionality over their profiles, as well as modify user settings 
    '''
    pass


def show_form(request):
    form = CustomerSignupForm()
    context = {
        'form': form,
    }
    return render(request, 'formtest.html', context)