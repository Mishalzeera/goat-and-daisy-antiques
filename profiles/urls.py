from django.urls import path
from . import views

urlpatterns = [

    path('', views.UserProfilePage.as_view(), name='profile'),
    path('login/', views.LoginUser.as_view(), name='login_user'),
    path('showform', views.show_form, name='showform'),

]