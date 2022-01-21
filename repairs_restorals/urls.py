from django.urls import path
from . import views

urlpatterns = [

    path('', views.Workshop.as_view(), name='workshop'),
    path('workbench/<int:pk>',
         views.CustomerWorkbench.as_view(), name='customer_workbench'),
    path('create-service-ticket/', views.CreateServiceTicket.as_view(),
         name='create_service_ticket')


]
