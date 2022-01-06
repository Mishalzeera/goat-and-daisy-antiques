from django.db import models


class Customer(models.Model):
    ''' 
    Any account created is basically an instance of this model with a one to one relationship with a User in the built in Django auth. 
    '''
    pass


class StaffMember(models.Model):
    '''
    Every member of staff can be described by this model, which determines their permissions within the custom CMS interfaces.
    '''