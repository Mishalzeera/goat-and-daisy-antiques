from django.urls import path
from . import views

urlpatterns = [

    path('', views.Workshop.as_view(), name='workshop'),
    path('workbench/<int:pk>',
         views.CustomerWorkbench.as_view(), name='customer_workbench'),
    path('create-service-ticket/', views.create_service_ticket,
         name='create_service_ticket'),
    path('add-image/', views.CustomerAddImage.as_view(), name='add_image'),
    path('ticket/<int:pk>/',
         views.ServiceTicketDetail.as_view(), name='service_ticket'),
    path('ticket-staff-only/<int:pk>/update/',
         views.ServiceTicketUpdate.as_view(), name="update_service_ticket"),
    path('ticket/<int:pk>/update/',
         views.PublicServiceTicketUpdate.as_view(), name="public_update_service_ticket"),
    path('ticket-overview/', views.WorkshopStaffTicketOverview.as_view(),
         name="ticket_overview"),
    path('confirm-delete/<int:pk>/',
         views.TicketDelete.as_view(), name="ticket_delete"),
    path('update-image/<int:pk>/',
         views.WorkshopStaffUpdateImage.as_view(), name="update_ticket_image"),
    path('delete-image/<int:pk>/',
         views.WorkshopStaffDeleteImage.as_view(), name="delete_ticket_image"),
    path('task-manager/', views.TaskManager.as_view(), name="task_manager"),
    path('manage-todo-item/<int:pk>/',
         views.delete_or_update_item_in_todo, name='manage_item'),

    path('admin-manage-todo-item/<int:pk>/',
         views.admin_delete_or_update_item_in_todo, name='admin_manage_item'),


    path('admin-task-manager/', views.AdminTaskCreate.as_view(),
         name='admin_task_manager'),

    path('admin-task-overview/', views.AdminTaskManagerOverview.as_view(),
         name='admin_task_overview'),

    path('customer-invoices', views.PublicCustomerInvoices.as_view(),
         name='customer_invoices'),
    path('all_customer_invoices/', views.AllCustomerInvoices.as_view(),
         name="all_customer_invoices"),
    path('customer_invoice_detail/<int:pk>/',
         views.AdminCustomerDetailView.as_view(), name="customer_invoice_detail"),
    path('admin-customer-invoice/<int:pk>/',
         views.AdminCustomerInvoice.as_view(), name='admin_customer_invoice'),
    path('delete-customer-invoice/<int:pk>/',
         views.WorkshopStaffDeleteInvoice.as_view(), name='delete_customer_invoice'),

]
