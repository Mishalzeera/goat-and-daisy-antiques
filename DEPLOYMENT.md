## Early deployment to Heroku

I created a test app that displays a simple HttpResponse when the server
navigates to '/'. 

Procfile contains 'web: gunicorn goat_and_daisy.wsgi'. 

Since I'm using pipenv, theres no need for 'requirements.txt', as Heroku 
supports pipenv.

Secret key is protected in a local file, which was added to the 'Config Vars'
in the Settings page of the Heroku project.

In the Deploy page of the Heroku project, the 'Connect To GitHub' option was
selected, and the correct repository connected from a drop-down list. Following
that, 'Automatic Deploys' was enabled, allowing any pushes to the GitHub repo
to take effect in the Heroku staging site.

Unfortunately, the first attempt to open the app results in the 'Welcome to
your new app' page, which is not what we are looking for. 

The logs repeatedly show desc="Blank app", which, according to the Heroku
docs is not an error strictly speaking. However, it isn't our index page, so
something is not right.

Turning to the Manual Deployment option, Heroku then attempted to build the
app from the repository. There were two issues, one pertaining to the 
secret_key variable, the other to do with static files. 

To rule out the static files being the main culprit, I copied and pasted the 
code Heroku suggested to bypass the issue. While the subsequent run revealed 
a different error, the secret key error remained. My focus then went to how
I coded the secret key conditional in settings.py.

For the moment, the conditional seems to resove the secret key error in the
build logs, but the static files error has increased in complexity. 

Adding the static files code snippet from Heroku back in caused the app to 
successfully build, however when running it the page reads "Internal Server
Error". According to the experience of some people on Stack Overflow, it could
be just the time it takes for Heroku to finish processing the app. 

In the meantime, I noticed that so many workarounds were offered for people
using the Heroku CLI. I downloaded and installed it, it will probably come in 
handy in the future.

Half an hour later, still no index page and the "Internal Server Error" is 
still there.

Four hours later, still no deployment. Its possible that since I added a 
Postgres addon (which hasn't been configured in the Django settings module)
the server is struggling. Trying to delete the Postgres key didn't work,
and Heroku refused to budge on that. So I erased the Heroku app entirely and
began again. First without the secret key environmental variable to be sure
that my settings conditional works as intended. This threw the previous error
with a 'secret_key not found' in the build logs, as well as a slew of messages
about the static files again. 

Adding the SECRET_KEY and value in the Config Vars allowed the app to build,
and according to the log, deploy. However, at the moment, our index page is 
still not showing and the "Internal Server Error" message is once again 
showing. 

After doing some research, it looks like Sqlite3 isn't supported by Heroku,
at least according to their docs. 

24 hours later, still not deployment. 

I created a new app, following the same procedures in a streamlined way, the 
new app deployed once the new Heroku url was added to "Allowed Hosts". The 
same code snippet for the static files management was necessary as well. It 
is clear that using SQLite, while probably causing issues down the
road, is not the obstacle to deployment.

Adding the Heroku URL to the path didn't solve the issue.

Best solution seems to be to begin again, deploy right away in the same manner
as the test app, and check as I build that whatever I do doesn't crash Heroku.


------------------


## New Project

Starting over, the same order of operations from the virtual environment, 
dependencies, Procfile, test app now works. It is possible that the issue was
the secret key encoding. I wasn't very clear on how environment vars worked
and still am not, but it makes much more sense now going over my code for the
Flask project. The next step will be to use the same process of creating an 
env file that sets an env variable and a if...exists conditional as well as
adding my key to the Config Vars in Heroku.

"os" was already imported at the top of the project settings, so the 
conditional to check the path for the env file was added. Env file was created
with the secret key set to a token hex created in the Python shell using the
"secrets" module. After checking on the local server and commenting out the
secret key assignment to check it fails otherwise, I then added the secret key
to the Heroku project. 

