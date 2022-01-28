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
    path('ticket/<int:pk>/update/',
         views.ServiceTicketUpdate.as_view(), name="update_service_ticket"),
    path('ticket-overview/', views.WorkshopStaffTicketOverview.as_view(),
         name="ticket_overview"),
    path('confirm-delete/<int:pk>/',
         views.TicketDelete.as_view(), name="ticket_delete"),
    path('task-manager/', views.TaskManager.as_view(), name="task_manager"),
    path('manage-todo-item/<int:pk>/',
         views.delete_or_update_item_in_todo, name='manage_item')



]
