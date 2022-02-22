debug = False!!

live emails

gmail> settings>accounts and import>Other Google account settings

Security> 2step verification

Security> App passwords

select mail and other

copy the passcode and go to Heroku

-config var EMAIL_Host_Pass 

-EMAIL_HOST_USER = your gmail

in settings use the if statement to distinguish prod and dev:

if DEV:
same email_backend
default_from_email = 'etcetc@g&d.com'

else:
email_backend = django.core.mail.backends.smtp.EmailBackend
email_use_tls = True
email_port = 587
email_host = 'smtp.gmail.com'
email_host_user = os.environ..get('email_host_user')
email_host_password = os..('email_host_pass')
default_from_email = os..('email_host_user')

then commit push


check that all of your user stories are satisfied and include a screenshot in the README to show what that looks like in your application.


403 page customise


