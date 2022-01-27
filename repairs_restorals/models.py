from django.db import models
from profiles.models import Customer, StaffMember


class ServiceTicket(models.Model):
    '''
    A current, open order for the workshop to complete - fields include customer, date created, service description, links to desired materials,
    images to show the desired outcome, is_completed.
    '''
    customer = models.ForeignKey(
        Customer, related_name='service_ticket', on_delete=models.PROTECT)
    workshop_staff_responsible = models.ForeignKey(
        StaffMember, related_name='staff_tickets', on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True, editable=False)
    last_updated = models.DateField(auto_now=True, editable=False)
    service_description = models.TextField()
    link_to_desired_materials_1 = models.URLField(null=True, blank=True)
    link_to_desired_materials_2 = models.URLField(null=True, blank=True)
    link_to_desired_materials_3 = models.URLField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class TicketImage(models.Model):
    '''
    An image related to a service ticket, uploaded by a customer, that shows 
    specifics about the kind of work desired.
    '''
    service_ticket = models.ForeignKey(
        ServiceTicket, related_name='images', on_delete=models.PROTECT)
    image = models.ImageField(upload_to="workshop/images/")

    def __str__(self) -> str:
        return str(self.service_ticket) + str(self.id)


class TodoList(models.Model):
    '''
    A list of "todo" items related to a single staff member.
    '''

    staff_member = models.ForeignKey(StaffMember, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.subject

class TodoItem(models.Model):
    '''
    An item in a "todo" list.
    '''
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title 
