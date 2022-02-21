| Test Label |Test Action  |Expected Outcome|Test Outcome|
|--|--|--|--|
|Navigate to site|Enter the base URL |Auto-redirects to **Index**|PASS |
|View **Shop** without signing in, prompted to do so when necessary or beneficial to do so|Navigating through the site, adding items to **cart**, navigating to **precheckout** |Upon seeing all the fields to fill out and realising how much easier it would be to sign in, convenient link handy, **sign in**, easy checkout|PASS|
|Fast, easy custom checkout|Click "**checkout**" at any point while signed in|Upon final payment page, all the information entered in the **registration page** shows up as **shipping address**|PASS|
|Positive feedback of **success page** and confirmation email (see Anon User MD for more detail)|Submit payment via G&D Stripe checkout and (being logged in to receive webhooks from Stripe and settings set to console email backend) check the console for emails|**Success** page reiterates the order details, **email** informs them that shipment is being prepared|PASS|
|Customer Order History |Navigate to **Profile** and view previous orders|A clear list of completed (shipped) orders and pending (on their way) |PASS|
|Seduction in the **Workshop** |Visiting the **Workshop** while signed in|Provide a clear message that G&D offers a robust and secure interactive repair/restoral service for customers with an account|PASS|
|Customer **Profile** CRUD|Click "View Profile" at any stage, update information or delete account|Customer has control over their account details in a straightforward way|PASS|