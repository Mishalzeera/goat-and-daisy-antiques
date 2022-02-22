from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('contact/', views.ContactUs.as_view(), name='contact_us')
]
