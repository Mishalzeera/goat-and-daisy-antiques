## One Site, Five Functions

It might be easiest to follow this sequence of explorations of the Goat And
Daisy website, as the interactions of users are interdependent. One example
is the workshop Service Ticket creation and related invoice creation.

## The Anonymous Shopper

Straightforwards browsing and adding things to cart, checking out.

Suggested steps to follow:

- Place an order or two.

## The Registered Shopper

Similar to the Anonymous Shopper, however shipping address etc is prefilled
in at checkout time.

Suggested steps to follow:

- Create an account and sign in.

- Place an order or two.

## The Registered Workshop Customer I

Access to the Workbench is restricted to registered users, which in turn
limits the creation of Service Tickets to registered users. The payment
flow is built around the interaction of staff and customer.

Suggested steps to follow:

- Create a separate customer account or continue with the current one.

- Navigate to Workbench, from the Workshop homepage.

- Create a service ticket. Add an image to it if you like.

- Sign out. We'll come back to this later.

## Shop Staff

Shop Staff have their own workflow settings, shown in the dropdown that
appears when someone with Shop Staff group settings is logged in.

- Sign in with "shop_staff" password "goat_daisy"

- View Shop Orders allows staff to keep track of items that have been
  sold, especially whether or not they have been shipped. You will see
  the orders you have tested in the earlier part of the walkthrough and
  some basic real-life processes like marking them as shipped/completed.

- Manage Inventory gives all CRUD functions to Shop inventory management.
  Images can be uploaded from a single page, in the case of having to upload
  multiple images for multiple items. They can also be added on a per-instance
  basis via each items CRUD links.

- Task Manager and All Registered Customers are under General Staff Permissions
  so they are shared by all employees.

- Task Manager is a basic todo app that can be overseen by admin.

- All Registered Customers is CRUD management for the Customer objects.

- Important: Sign out!

## Workshop Staff

Workshop staff access their functionality by signing in as a staff
member with workshop group permissions.

- Sign in with "workshop_staff" password "goat_daisy". In the dropdown:

- View Customers and Tickets lets you keep track of each customers details
  while keeping their Service Tickets handy. There is some CRUD available.
  Organised by Customer >Current Tickets >Completed Tickets.

- Manage Invoices contines where we left off as a Workshop Customer. Here
  you will see the Ticket or Tickets you created earlier. You can now, as
  staff, assess the amount of work/supplies etc needed and update the
  auto-generated invoice with an amount. More on this later, when you
  sign back in as Workshop Customer.

- Task Manager and All Registered Customers are identical to Shop Staff.

## The Registered Workshop Customer II

Continuing where we left off with the customer experience - imagining
that some time has gone by. A buys artisan has looked at your request,
your supplies and your images and has given you a quote.

- Sign back in as your customer with Service Tickets account.

- Go to your Workbench, which is accessed from the Workshop homepage.

- Click View/Pay Invoices

- Under outstanding invoices, you will find your new invoice, which
  is by default a Deposit. However, if you discussed it with a staff
  member, he/she can also have created a Single Payment Total or
  a custom deposit (Single Payment).

- Click Pay invoice, follow the checkout process.

- If it was a deposit, the webhook handler will create an endpayment invoice
  which will appear in your View/Pay Invoices as and when Workshop
  Staff has finished the work and approved the final payment amount.

- At this point, there will be a record of your having paid in the
  View/Pay Invoices page.

- You may only update Tickets with links at this point, which allows you
  to specify the materials for the staff to source. In NICE_TO_HAVE.md is
  some discussion about how to streamline this with the input of a real
  business owner.

- Optionally, you can sign out and sign in again as workshop_staff password
  goat_daisy and further explore the payment process.

## Admin

From the start I thought it might be a good experience to limit the true
Django Admin panel to admin only. In my visualisation of the workflow at
that point, it made sense. Looking back, maybe a bit too time consuming.

Admin's toolbox is accessed via logging in with admin permissions.

- Staff Management gives Admin an easy way to register staff without
  having to scroll through lots of users. I used Django built in Auth
  for this project, so both the Customers and the Staff Members have profiles
  linked to Auth accounts. Admin can set staff permission groups quite easily at
  this point, and update them at any time.

- View Staff gives some easy CRUD for those kinds of things. There are staff notes
  and admin only notes as well, for other admin users.

- Links to Admin panel.

- Task Manager Overview at this moment is perhaps a bit in the Kim Jong-Il style
  of management. NICE_TO_HAVE goes into this a bit. At the moment, Admin can have
  some idea of where employees are with certain projects. In the future, it makes
  sense to have it so that Admin can issue todo-lists, and view only admin-issued
  lists.
