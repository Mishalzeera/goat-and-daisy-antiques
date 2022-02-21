| Test Label |Test Action  |Expected Outcome|Test Outcome|
|--|--|--|--|
|Navigate to site|Enter the base URL |Auto-redirects to **Index**|PASS |
|Special Shop Staff nav dropdown|Log in Staff Members with Shop Staff perms|Upon login, gain access to unique links - View Shop Orders, Manage Inventory, Task Manager, All Registered Customers|PASS|
|View Shop Orders|Follow the link|A clear interface with two columns - Orders to ship (each with a "mark completed" function which pushes them to) Completed orders |PASS|
|Manage Inventory|Follow the link|A page which allows Shop Staff to create new inventory items, add images and edit all relevant fields|PASS|
|Task Manager|Follow link|Gives staff a handy tool to keep track of multiple projects, marking each list item as complete as and when needed|PASS|
|All Registered Customers|Follow the link|A list of all current customers in the database, shared between all staff (General Staff group perms)|PASS|
|Limit Admin access|Attempt to login to Django admin panel|Shop Staff will be denied access (unless Admin allows per-case-basis)|PASS|