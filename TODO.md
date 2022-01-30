## Profiles

- check out any tutorials on permission mixins
- phonenumber
- find programmatic way to automatically add staff members to correct groups
- learn more about signals and see if that might help the signup registration
  process Code With Mosh Django2 Designing and Building Api 11
- remember on models.py to check/change the get_absolute_url setting

## Site Layout

-Create custom Navs for each part of the site

## Shop

- work out the images from templates

## Repairs/Restorals

-Make staff service ticket Create view and form
-ticket update for customer restricted to links

- determine if a customer has a ticket, then provide that customer with a nav
  link to a ListView tickets page, then a ticket to modify
- for staff, a dropdown menu to a list of tickets as well as one to active
  workshop customers, staff to edit all, dropdown that shows customer and
  related tickets.
- ticket list leads to customer profile
- customer list leads to valid tickets
- do something about the hardcoded workshop_staff in
  CreateServiceTicket views.py

- for todo list, make it for every user
- make sure that new customers dont see Current and Completed Tickets

## Invoices

-customer create order/invoice
-customer view order/invoice
-shop staff create order/invoice
-shop staff view invoices

- service ticket on save if not invoice create invoice, default=deposit
- customer view invoice
- staff view/update invoice

- when shop customer adds an item to their order, if_available is set to False
  for fifteen minutes
