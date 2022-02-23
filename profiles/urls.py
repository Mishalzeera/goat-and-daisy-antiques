from django.urls import path
from . import views

urlpatterns = [

    path('<int:pk>/', views.CustomerProfilePage.as_view(), name='customer_profile'),
    path('login/', views.LoginAUser.as_view(), name='login_user'),
    path('signup/', views.UserSignupPage.as_view(), name='signup'),
    path('create-profile/', views.CreateProfilePage.as_view(), name='create_profile'),
    path('staff-signup/', views.StaffMemberSignupPage.as_view(), name='staff_signup'),
    path('create-staff-profile/', views.CreateStaffProfilePage.as_view(),
         name='create_staff_profile'),
    path('change-password/', views.ChangePassword.as_view(), name="change_password"),
    path('password-changed/', views.password_changed, name="password_changed"),
    path('all-staff/', views.AdminStaffList.as_view(), name="all_staff"),
    path('staff-update/<int:pk>/', views.AdminStaffUpdate.as_view(),
         name="admin_staff_update"),
    path('private-customer-update/<int:pk>/', views.CustomerAccountUpdate.as_view(),
         name="customer_account_update"),
    path('customer-update/<int:pk>/', views.PublicCustomerAccountUpdate.as_view(),
         name="public_customer_account_update"),
    path('account-confirm-delete/<int:customer_id>/',
         views.pre_delete, name="pre_delete"),
    path('account-delete/<int:customer_id>/',
         views.delete_profile, name="delete_profile"),
    path('admin-overview/', views.AdminOverview.as_view(), name='admin_overview'),
    path('staff-member/<int:pk>/', views.StaffMemberDetailView.as_view(),
         name='view_staff_member'),

]
