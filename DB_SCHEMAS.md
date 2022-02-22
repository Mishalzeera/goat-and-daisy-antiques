Schema of database and model methods

## Invoices

**Base Invoice:**
date_created = DateField
order_number = CharField
full_name = CharField
email = EmailField
address1 = CharField
address2 = CharField
postcode = CharField
town_or_city = CharField
country = CharField
notes = TextField
order_amount = DecimalField
shipping_cost = DecimalField
order_total = DecimalField
is_completed = BooleanField(default=False)
paid_on = DateTimeField

-generate_order_number = unique order number per order
-generate_timestamp = datetime timestamp
-calculate_order_total = adds relevant fields

**Shop Customer Invoice**
-identical to Base Invoice, planned customisation was unnecessary
but semantic name was useful

**Workshop Customer Invoice**

service_ticket = ForeignKey(ServiceTicket)
payment_type = CharField
installment_paid = BooleanField

-set_has_invoice_to_true = distinguish tickets without invoices

## Profiles

**Customer**

username = OneToOneField(User)
email = EmailField
full_name = CharField
address1 = CharField
address2 = CharField
postcode = CharField
town_or_city = CharField
country = CharField
notes = TextField
staff_notes = TextField
has_active_shop_orders = BooleanField
has_active_repairs = BooleanField

**Staff Member**

username = OneToOneField(User)
email = EmailField
full_name = CharField
shop_staff = BooleanField
workshop_staff = BooleanField
admin_access_permission = BooleanField
notes = TextField
admin_notes = TextField
default_workshop_staff = BooleanField

## Repairs/Restorals

**Service Ticket**

customer = ForeignKey(Customer)
workshop_staff_responsible = ForeignKey(StaffMember)
title = CharField
date_created = DateField
last_updated = DateField
service_description = TextField
link_to_desired_materials_1 = URLField
link_to_desired_materials_2 = URLField
link_to_desired_materials_3 = URLField
is_completed = BooleanField
has_invoice = BooleanField

**Ticket Image**

service_ticket = ForeignKey(ServiceTicket)
image = ImageField

**Todo List**

staff_member = ForeignKey(StaffMember)
subject = CharField

**Todo Item**

todo_list = ForeignKey(TodoList)
title = CharField
is_completed = BooleanField

## Shop

**Shop Items**

- unfortunately a plural title and changing it later caused too many issues

title = CharField(max_length=255)
description = TextField
price = DecimalField
shipping = DecimalField
is_available = BooleanField

**Shop Item Image**

product = ForeignKey(ShopItems)
is_primary_image = BooleanField
image = ImageField

-set_one_to_default = checks if no other images exist and sets itself to promary image
