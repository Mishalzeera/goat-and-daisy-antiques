## Profiles

- current orders to customer profiles
- no notes to new customer profile setup

- check out any tutorials on permission mixins
- phonenumber
- find programmatic way to automatically add staff members to correct groups
- remember on models.py to check/change the get_absolute_url setting

## Site Layout

## Shop

-precheckout page with shopper information that creates an invoice and then
redirects to actual checkout page, allowing the shipping info to be saved in an
invoice, which is then accessed by a webhook handler to create follow up

OR

- embed the shipping info in the metadata which is messier down the line


- after order, create completed order invoice saved as paid

- add shipping to ShopItems

- cookie session expiry for a specific cookie

## Repairs/Restorals

-Make staff service ticket Create view and form

- email deposit invoice to customer, if total is 0, its an email
  saying staff is assessing the work and will give a quote and send an invoice
  otherwise an email to customer with everything

- do something about the hardcoded workshop_staff in
  CreateServiceTicket views.py

- for todo list, make it for every user
- make sure that new customers dont see Current and Completed Tickets

## Invoices

- Update Cart/Remove from cart
  -customer create order/invoice
  -customer view order/invoice
  -shop staff create order/invoice
  -shop staff view invoices

- customer view invoice
- staff view/update invoice

403 page customise
HTTPS HTTPS HTTPS
