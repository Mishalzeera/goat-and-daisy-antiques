from django.urls import path
from . import views

urlpatterns = [

    path('', views.UserProfilePage.as_view(), name='profile')

]