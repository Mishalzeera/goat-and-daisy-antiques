# Such a pain in the proverbial that it deserves its own MD file

## The idea

- The server side code generates an instance of PaymentIntent.
  It gets request.data from the request object, which is turned into JSON.

I have received errors here saying there is no 'data' attribute, but not always.

The instance of Payment Intent goes into a variable 'intent'.

In its creation the instance has 'amount=', 'currency',
'automatic_payment_methods='. Amount so far I have set to the request.session
order_total.

I should try a hardcoded example first.

The function returns a json response of a dictionary, where a javascript
style variable 'clientSecret' is set to the intent['client_secret']

- The template has two divs that go inside a form with specific ids. The form
  is also given a specific id.

The general Stripe JS API link is put in the base template's head

The newer Stripe makes no mention of any extra js links than a single file.

- The javascript file creates an instance of Secret using the Public Key.

A const items, something hardcoded, Im guessing to test. Looks like a list of
dictionaries, but there is just one dictionary in the list.

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


