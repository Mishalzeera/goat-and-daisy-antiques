from django.contrib import admin
from .models import ServiceTicket, TicketImage, TodoList, TodoItem

admin.site.register(TicketImage)


@admin.register(ServiceTicket)
class ServiceTicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'staff_member', 'is_completed']

    def staff_member(self, service_ticket):
        return service_ticket.workshop_staff_responsible
