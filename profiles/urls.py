from django.urls import path
from . import views

urlpatterns = [

    path('', views.UserProfilePage.as_view(), name='profile'),
    path('login/', views.LoginAUser.as_view(), name='login_user'),
    path('signup/', views.UserSignupPage.as_view(), name='signup'),
    path('admin-overview/', views.AdminUserManagement.as_view(), name='admin_overview'),

]