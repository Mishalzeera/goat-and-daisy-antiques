| Test Label |Test Action  |Expected Outcome|Test Outcome|
|--|--|--|--|
|Navigate to site|Enter the base URL |Auto-redirects to  **Index**|PASS |
|All the functions of registered Shop user |Browse **Shop** and add items, checkout with all the functions in the REG_SHOP_USER md file|Identical experience to registered Shop user|PASS|
|Find Workbench|Navigate to **Workshop** while signed in |Clear link to customer **Workbench**|PASS|
|Create a Service Ticket|Click Create Service Ticket|A form appears where the customer can create a new **Service Ticket**|PASS|
|Email confirmation|While settings sends emails to the console backend, check the terminal|An email is automatically sent to customer informing them that a quote is being prepared for a deposit (which is created automatically via a signal - see WORKSHOP_STAFF md)|PASS|
|Add **Image to Ticket**|Click "Add Image To Tickets" in Workbench|Straightforward upload of images to ticket|PASS|
|Update/add links to Ticket|Click "Update" on a Service Ticket|Blank fields to upload **new URLS for products/materials** to order|PASS|
|Pay deposit|Click "**View/Pay invoices**" in customer **Workbench**|Simple and clear interface with links to pay outstanding invoices (in this case deposit but most of this is determined by Workshop Staff - see WORKSHOP_STAFF md)|PASS|
|Email confirmation|While settings sends emails to the console backend, check the terminal|An email is automatically sent to customer informing them that an endpayment invoice is being prepared (see WORKSHOP_STAFF md)|PASS|
|View **history**|Navigate to "View/Pay Invoices"|Clear, simple view of completed orders and paid invoices|PASS|



