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

- image = models.ImageField(upload_to="name of what directory you want to add
  to the media root automatically")

## Using CreateView to post a form with hidden username/email etc

- In the view, use def form_valid to assign 'form.instance.key' = 'value',
  setting any queried values before hand eg 'customer = Customer.objects...'

- In the model form, exclude the fields you don't want the user to tamper with.

- Sometimes function based views are just a lot better and easier if you want
  to write custom logic

## Limiting a Model Form set of options to request.user's

- If using CBV's then get_form_kwargs needs to be rewritten..
  https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-
  form-classes-ee322f02948c

- Finally, using form.fields['field'].queryset = ... in the views did it.

## Images, function based views..

- enctype="multi..." must be in template form tag

- form = MyForm(request.POST, request.FILES) in order for it to upload

## Creating custom signal integrated with model methods

Create 'signals.py' in relevant app. In apps.py override the ready(self) method
with 'import relevant_app.signals'.

Potential issue with writing objects.create() directly causing it to loop
infinitely.

Use an if statement checking an object exists, then execute the block.

## Shopping cart, request.session, context processor

Setting up a context processor, adding it to the context
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

https://realpython.com/intro-to-python-threading/

Mainly, args can be sent, and this daemon thing can be set, and the Thread
can be instantiated within the context of the function concerned. A target
function is defined outside the function, that target is the process that is
kept apart from the main thread flow of the program.

Without taking the item out of the customers sessioncookie, 
multiple purchases might happen of the same item. A settings config
variable CUSTOMER_SESSION_EXPIRY was created, with a integer defining how many
seconds. The variable was then used in the add to cart view, both to set the
timer for the "is_available" attribute of the reserved shop item as well as
the general expiry date of the users session.
