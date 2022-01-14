from django.urls import path
from . import views

urlpatterns = [

    path('<int:pk>/', views.CustomerProfilePage.as_view(), name='customer_profile'),
    path('login/', views.LoginAUser.as_view(), name='login_user'),
    path('signup/', views.UserSignupPage.as_view(), name='signup'),
    path('create-profile/', views.CreateProfilePage.as_view(), name='create_profile'),
    path('staff-signup/', views.StaffMemberSignupPage.as_view(), name='staff_signup'),
    path('create-staff-profile/', views.CreateStaffProfilePage.as_view(), name='create_staff_profile'),
    path('all-customers/', views.AllCustomers.as_view(), name="all_customers"),
    path('all-staff/', views.AdminStaffList.as_view(), name="all_staff"),
    path('staff-update/<int:pk>/', views.AdminStaffUpdate.as_view(), name="admin_staff_update"),
    path('customer-update/<int:pk>/', views.CustomerAccountUpdate.as_view(), name="customer_account_update"),

]