# Hello and welcome

## Docs

There are a few docs explaining the steps and details of issues relating to
deployment and Stripe API integration. These will be found in the
md files in the file explorer.

However you might like to have some basic things to look out for.

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
the if DATABASE code before handling any version control.

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

## Admin Task Manager

The task manager sometimes does not behave as it should.

When the red warning Required is showing in the main form, it will work ok
on its first use.

If the page loads and the red Required is missing, then it won't create new lists
or show the queryset.

Something to look into.

## Site Walkthrough

You may find it helpful to follow the SITE_WALKTHROUGH.md file step by step to
become familiar with the workflow of the site. Some things may not make sense
until you see an action through.

## Process Notes

If you aren't familiar or are new to Django, like myself, read PROCESS_NOTES. It
covers a lot of issues dealing with Heroku Deployment, Django Class Based Views,
Django Auth as well.

If you are familiar with Django, reading it might give you an idea where I
may have gone wrong in places, causing issues you are now trying to
troubleshoot.
