from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.views import UserProfilePage, UserSignupPage, AdminUserManagement
from profiles.models import Customer, StaffMember 
from profiles.forms import UserAuthAccountCreationForm, CustomerSignupForm, AdminStaffManagementForm, StaffUserManagementForm
import json

 
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('index')
        self.signup_url = reverse('signup')
        self.user_auth_account_creation_form = UserAuthAccountCreationForm()
        self.customer_signup_form = CustomerSignupForm()
        self.admin_staff_management_form = AdminStaffManagementForm()
        self.staff_user_management_form = StaffUserManagementForm()
        self.auth_example_user = User.objects.create(
            username = 'testusername',
            email = 'testemail@domain.com',
            password = 'testpassword123!'
        )


    def test_UserProfilePage_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'site_layout/index.html')


    def test_UserSignupPage_GET(self):
        response = self.client.get(self.signup_url)
        form = self.user_auth_account_creation_form
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        


    # def test_UserSignupPage_POST(self):

