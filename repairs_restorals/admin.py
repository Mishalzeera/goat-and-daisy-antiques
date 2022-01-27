from django.contrib import admin
from .models import ServiceTicket, TicketImage, TodoList, TodoItem

admin.site.register(TicketImage)


@admin.register(ServiceTicket)
class ServiceTicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'staff_member']

    def staff_member(self, service_ticket):
        return service_ticket.workshop_staff_responsible


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ['staff_member', 'subject']


@admin.register(TodoItem)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_completed']
