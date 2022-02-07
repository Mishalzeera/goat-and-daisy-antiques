## Heroku deployment

-Deploy early with minimal apps and views.
-pipenv install django-heroku
-pipenv install gunicorn (Check Deployment.md for more)
-Ensure secret key is set as an env variable in a os.path.exists("env.py") file.
-Use the code snippet from Heroku to create a separate staticfiles dir that
-Heroku can use to copy files to.
-Install whitenoise to allow Heroku to directly serve your static files at least
during production.

## Using built in Django Auth module

-Make sure the template path in settings is added to the project level, and
create a templates>registration>login.html for login etc. Log out is called
logged_out.html.

## Using Django's Class Based Views

-Make sure you use each one correctly, View has "get" and "post" methods, for
example, while many others don't. Overriding attributes and methods is the key
to using them correctly. In template forms, setting the "action" attribute to
a fullstop "." is the correct way to use something like a Create or Update view
which needs only the model, form and fields to auto-generate the form and data
pathways. Very handy and quick but only once you understand it.

-With permissions, you can use mixins as well as decorators. The decorators go
in the urls.py file, and decorate the view reference in the "path" structure.
eg. path('', permission_required('appname.can_add_etc')(MyCBView.as_view())),
importing permission_required from contrib.auth.decorators.

## Custom tag filters

-In the relevant app, a folder must be called 'templatetags' and contain an
**init**.py file. Another file must be created, the tag registered within, then
the filename is referenced in the template as load 'filename'. Then any tags
named in that file will be accessible. Be sure to restart the server.

## Adding images

- Using Media since there is changing CMS content used by staff without admin
  privileges. MEDIA_URL = "/media" MEDIA_ROOT = os.path.join(BASE_DIR, 'static')
  Add a context processor 'django.template.context_processors.media', in templates
  everything uploaded there will be available as

<img src="{{ MEDIA_URL }}example.jpg">

- In main project directory urls.py, from django.conf import settings, from
  django.conf.urls.static import static, then

if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

- In models, an image model with a 'product' field, ForeignKey, related_name=
  images, return def \_\_str as str(self.product) + str(self.id) for now.
- image = models.ImageField(upload_to="name of what directory you want to add
  to the media root automatically")

## Using CreateView to post a form with hidden username/email etc

- In the view, use def form_valid to assign 'form.instance.key' = 'value',
  setting any queried values before hand eg 'customer = Customer.objects...'

- In the model form, exclude the fields you don't want the user to tamper with.

- Sometimes function based views are just a lot better and easier if you want
  to write custom logic

  ## Limiting a Model Form set of options to request.user's

  - Very tricky, if using CBV's then get_form_kwargs needs to be rewritten..
    https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-
    form-classes-ee322f02948c

  - Also an **init** override method which was too complicated in accessing
    request.user

  - Finally, using form.fields['field'].queryset = ... in the views did it. Not
    so tricky in the end but finding the solution was about four hours of
    trial and error.

  ## Images, function based views..

  - enctype="multi..." must be in template form tag

  - form = MyForm(request.POST, request.FILES) in order for it to upload

  ## Empty screen on redirect from function view

  - The following code caused an error that I could not debug after many hours,
    in the interest of saving time I have reverted to using Class Based View but
    will ask someone:

  views.py>

  # def customer_add_image(request):

# if request.method == 'GET':

# '''

# The GET method must return an image upload form with two fields. One

# field is a list of request.users tickets. Once a ticket is selected,

# the user can upload an image which will be linked to that ticket

# '''

# form = CustomerUploadImageForm()

# customer = get_object_or_404(Customer, username=request.user)

# form.fields['service_ticket'].queryset = ServiceTicket.objects.filter(

# customer=customer)

# context = {

# 'form': form,

# }

# return render(request, 'repairs_restorals/add_image.html', context)

# if request.method == 'POST':

# '''The POST method creates an instance of a TicketImage via the

# upload form and saves it'''

# form = CustomerUploadImageForm(request.POST, request.FILES)

# if form.is_valid:

# form.save()

# return render(request, 'repairs_restorals/add_image.html')

urls.py>

# path('add-image/', views.customer_add_image, name='add_image'),

add_image.html>

{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}

<h1>Add Images To Your Tickets</h1>

<form action="." method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form | crispy }}
    <input type="submit" value="Add Image">
</form>

{% endblock %}

## Creating custom signal integrated with model methods

Seeing the integration between model methods and signals, and running into
circular import errors when trying to use only model methods, I decided to try
using signals to auto-generate an invoice in the case of a Workshop Service
Ticket being created.

This was tricky, not least for identifying the request.user, which I did by
referencing the Customer database with the instance.username. The main issue
was actually that writing the WorkshopCustomerInvoice.create() directly
caused it to loop infinitely.

This made my database populate endlessly with new objects until I cut the
server. Made worse by the fact that there was no data for the admin panel to
display, which throws an error when you try and delete them.

Going into the shell, creating a list with objects.all() and iterating through
them, adding a displayable name and saving per-instance, then going into the
admin panel and deleting them as normal worked.

The solution in the signals code was to use IF an object with that name didn't
exist (filtering service_ticket_id with instance.id) then execute the block.

## Shopping cart, request.session, context processor

Main issue in implementation was in the add_to_bag view, not correctly using
dictionary syntax. Be sure to add a new dict as a value to a new key, so the
dictionaries nest properly. Eg.. its not old_dict.append(new_dict) which wont
work anyway. Its old_dict[a_key_based_on_unique_id] = new_dict. Would have
saved me three days if I just grasped that a bit better.

Other than that, setting up a context processor, adding it to the context
processors in SETTINGS>TEMPLATES>OPTIONS>'context_processors'>
'appname.filename.functionname'.

Everything is then instantiated immediately upon login or navigation to the
site, so bear that in mind.

## Threading: timer going on in the background

When a store item is put in a shopping cart, it should give the customer a 
period of time where they can purchase with certainty despite maybe having to
find a credit card or check their address. 

The idea was to create a toggle "is_available" function with a timer. However,
it wasn't that simple. Doing it that way caused the entire application to 
freeze for the duration of the timer - bypassing the actual functionality
I needed it to do in the first place.

There was multiple reference to Celery in the Stack Overflow community. However,
it seemed like overkill to install yet another package to accomplish just this 
one thing.

Looking up "async code in Python" on the other hand, introduced me to the 
concept of threading. Namely, one can create a process that goes on in its own
context, without messing up the overall flow of the code.

https://realpython.com/intro-to-python-threading/

The link above is full of very thick jargon, but some of the key concepts
made sense right away, after mucking about with another source's interpretation.

Mainly, args can be sent, and this daemon thing can be set, and the Thread
can be instantiated within the context of the function concerned. A target 
function is defined outside the function, that target is the process that is 
kept apart from the main thread flow of the program.

