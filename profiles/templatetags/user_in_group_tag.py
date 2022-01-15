'''
from:
https://stackoverflow.com/questions/34571880/how-to-check-in-template-if-user-belongs-to-a-group

In template:
{% load has_group %}

{% if request.user|has_group:"mygroup" %} 
    <p>User belongs to my group</p>
{% else %}
    <p>User does not belong to my group</p>
{% endif %}

'''


from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()