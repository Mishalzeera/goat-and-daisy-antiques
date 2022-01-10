from django.test import SimpleTestCase
from django.urls import reverse, resolve 
from profiles.views import UserProfilePage, UserSignupPage, AdminUserManagement


class TestUrls(SimpleTestCase):

    def test_profiles_url_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func.view_class, UserProfilePage)

    
    def test_signup_url_is_working(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, UserSignupPage)

    
    def test_admin_user_management_url_is_working(self):
        url = reverse('admin_overview')
        self.assertEquals(resolve(url).func.view_class, AdminUserManagement)
