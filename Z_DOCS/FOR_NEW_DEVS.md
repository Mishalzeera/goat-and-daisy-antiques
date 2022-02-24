# Hello and welcome

## Docs

There are a few docs explaining the steps and details of issues relating to
deployment and Stripe API integration. These will be found in the
md files in the file explorer.

However you might like to have some basic things to look out for.

## Site Walkthrough

You may find it helpful to follow the SITE_WALKTHROUGH.md file step by step to
become familiar with the workflow of the site. Some things may not make sense
until you see an action through.

## Pipenv

When working with this application in the terminal, please type pipenv shell
before doing anything. To install any packages, use 'pipenv install' instead
of 'pip/pip3 install'.

## Prod vs Dev migrations

When you are working locally on this site, don't forget that the database you
will be using is the sqlite one that Django installed. It will not be the
production Postgres database.

This means your migrations won't be applied to the Production db if you
make any key changes to your models.

Keep an alternative DATABASES setup which has your Postgres data in it
stored in your .env file. When needs be just copy and paste it into settings.
Then comment out the if statement regarding DATABASES. Now when you run
migrations, the database being migrated will be your Production one.

Please remember to erase the sensitive DATABASE setting and uncomment-out
the if DATABASE code before using any version control.

## In Devmode testing webhooks..

Using the Stripe Cli is much easier when working locally - simply download the
Cli from the Stripe website, open a fresh terminal, cd into the directory where
you have saved the file.

Then type .\stripe login, follow the steps for logging in.

Then type .\stripe listen --forward-to 'your webhook url including all local
prefixes' For instance, for me it has been http//:127.0.0.1:8000/invoices/wh/

Once thats working, you can run all your webhook functions.

If you run out of shop items to test, run 'pipenv shell', then 'python3 manage.py
shell'. In the shell, type 'from shop.models import ShopItems', then assign a
variable (eg 'items') to ShopItems.objects.all(). Iterate through the list,
setting each iteration to True and saving each iteration. You may need to do this
quite often to troubleshoot Stripe related issues in general.

## Testing

Testing badly needs to be written for this app. If a few tests can be written
here and there it should be done before too long.

## ShopItems

The ShopItems model, if F2'd into ShopItem, does not smoothly translate. Due
to time constraints I was unable to debug the issue. It could be a simple fix
but proceed with care.

## Customer Session Expiry

If you notice that after adding or removing items in the cart that your session
expires, this is to do with the CUSTOMER_SESSION_EXPIRY variable set in the
settings module. This figure in seconds is used by the cart functions to
release an item into the shop if it isn't bought by a certain time.

Unfortunately, the only workable option within the time constraint was using
a method that basically wipes the whole request session at the end of the time
period. You won't be logged in and anything in your session will be reverted
to null.

## Process Notes

If you aren't familiar or are new to Django, like myself, read PROCESS_NOTES. It
covers a lot of issues dealing with Heroku Deployment, Django Class Based Views,
Django Auth as well.

If you are familiar with Django, reading it might give you an idea where I
may have gone wrong in places, causing issues you are now trying to
troubleshoot.
