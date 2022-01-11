from django.test import TestCase, Client
from django.urls import reverse
from profiles.views import UserProfilePage, UserSignupPage, AdminUserManagement
from profiles.models import Customer, StaffMember 
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('index')
        self.signup_url = reverse('signup')

    def test_UserProfilePage_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'site_layout/index.html')


    def test_UserSignupPage_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')


    # def test_UserSignupPage_POST(self):

