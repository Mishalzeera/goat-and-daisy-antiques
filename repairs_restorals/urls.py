from django.urls import path
from . import views

urlpatterns = [

    path('', views.Workshop.as_view(), name='workshop'),
    path('workbench/<customer_pk>', views.CustomerWorkbench.as_view, name='workbench'),
    path('workbench/ticket/<ticket_pk>', views.ServiceTicket.as_view(), name='ticket')


]