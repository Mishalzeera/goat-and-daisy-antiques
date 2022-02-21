| Test Label |Test Action  |Expected Outcome|Test Outcome|
|--|--|--|--|
|Navigate to site|Enter the base URL |Auto-redirects to **Index**|PASS |
|Special Workshop Staff nav dropdown|Log in Staff Members with Workshop Staff perms|Upon login, gain access to unique links - View Customers And Tickets, Manage Invoices, Task Manager, All Registered Customers|PASS|
|View Customers And Tickets|Follow link|CRUD functions related to Service Tickets, organised by Customer|PASS|
|Manage Invoices|Follow link|Update existing invoices created by signal when Workshop Customer creates a Service Ticket - giving it an amount to pay, which then shows up in Customer's Workbench. Also setting it to either Deposit or varied options, which affects the payment flow. |PASS|
|Task Manager|Follow link|Gives staff a handy tool to keep track of multiple projects, marking each list item as complete as and when needed|PASS|
|All Registered Customers|Follow link|A list of all current customers in the database, shared between all staff (General Staff group perms)|PASS|
|Limit Admin access|Attempt to login to Django admin panel|Workshop Staff will be denied access (unless Admin allows per-case-basis)|PASS|