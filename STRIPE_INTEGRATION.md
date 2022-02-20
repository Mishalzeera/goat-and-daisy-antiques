## The concept

- The server side code generates an instance of PaymentIntent.
  It gets request.data from the request object passed from Stripe,
  which is recieved as JSON.

I have received errors here saying there is no 'data' attribute, but not always - its
a Django vs Flask thing. Flask uses request.data in this instance while Django uses request.body

The instance of Payment Intent goes into a variable 'intent'.

The function returns a json response of a dictionary, where a javascript
style variable 'clientSecret' is set to the intent['client_secret']

- The template has two divs that go inside a form with specific ids. The form
  is also given a specific id.

The general Stripe JS API link is put in the base template's head

The newer Stripe makes no mention of any extra js links than a single file.

- The javascript file creates an instance of Secret using the Public Key.

A const items, something hardcoded, Im guessing to test. Single object.

elements is let, with no assignments.

Two functions are called, initialize() and checkStatus()

The form is listened to for a submit event, in which case 'handleSubmit' is to
be called.

The function for intialize is defined then - until a response is fetched from
a specific url that should be where the server logic is. The Post method,
some security headers and in the body : the 'items' list previously mentions in
a string-formatted JSON form.

The const clientSecret is then given the response back

The main error I have is that there is no clientSecret, so something isn't
coming back from the server function.

## Important CSRF workaround

- Handling the CSRF token issue - Django will not allow any POST activity
  without a csrf_token. The Stripe Javascript makes its own POST request, so
  this is how you do it:

- In the template itself, place a {% csrf_token %} wherever it is unobtrusive.

- In the javascript, query the element and store it in a variable:

const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

- Then in the initialize function, add 'X-CSRFToken': csrftoken to the 'headers'
  dictionary.

## json.loads(request.data) should be json.loads(request.body)

- The main culprit once the csrf token was fixed.

## Having it figured out == FALSE

- The JS handles an important part of the payment intent creation. "Items" is
  a hardcoded variable that is passed into a placeholder function, with some
  commented out suggestions from Stripe to replace it with your own order total
  creation.

- The placeholder function is used in the create payment intent function, which
  I have routed somewhere else. I will keep it that way since its working for
  now.

## Webhooks, CLI and troubleshooting

- Moving your Django development setup to another system, laptop Gitpod etc
  can be a major pain, so best to use the Stripe CLI in the interest of saving
  time.

- An important issue with adapting the code from the Stripe website has been
  ensuring that wherever 'data' appears as an attribute, this should be changed
  to 'body'. Its possible this is a Flask vs Django thing.

- Set up the CLI, you have to navigate to the directory that the downloaded
  file is in, to use it. Easiest with CMD rather than the VS code terminal.

- In the first one: stripe listen --forward-to localhost:8000/invoices/wh
  (thats the Url of your post only, csrf exempt webhook function)

- In a second window: stripe trigger payment_intent.succeeded (or whichever
  event you want to trigger) - just to test basic signals

- You have to log in and have the CLI listening to the correct url - then you
  can inspect the metadata etc, work on the event handling and all that.

- It doesn't just work without being set up correctly, including the webhook
  secret key and being logged in.
