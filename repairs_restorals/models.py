from django.db import models


class ServiceTicket(models.Model):
    '''
    A current, open order for the workshop to complete - fields include customer, date created, service description, links to desired materials,
    images to show the desired outcome, is_completed
    '''
    pass