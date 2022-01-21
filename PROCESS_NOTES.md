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
__init__.py file. Another file must be created, the tag registered within, then
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
images, return def __str as str(self.product) + str(self.id) for now.
 - image = models.ImageField(upload_to="name of what directory you want to add
 to the media root automatically")

## Using CreateView to post a form with hidden username/email etc

- In the view, use def form_valid to assign 'form.instance.key' = 'value', 
 setting any queried values before hand eg 'customer = Customer.objects...'

- In the model form, exclude the fields you don't want the user to tamper with.

- Sometimes function based views are just a lot better and easier if you want
  to write custom logic