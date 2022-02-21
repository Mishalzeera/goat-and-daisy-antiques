
| Test Label |Test Action  |Expected Outcome|Test Outcome|
|--|--|--|--|
|Navigate to site|Enter the base URL |Auto-redirects to 'index' - **Index**|PASS |
|Gain overview of site contents|Select links of interest in the nav element|Switches between shop and workshop|PASS|
|Made aware of opportunity to create accounts, and benefits where pertinent|Prompts in all pages as well as nav|Clearly discern where and when having an account is useful as well as possible|PASS|
|Browse shop items as anonymous user|Navigate to shop and browse items in detail, with option to add to cart|View products that are available (no double purchases) and examine them in detail|PASS|
|Add and remove items in cart, keep track of cart contents|Check "View Cart" link, interact with shop "Add To Cart" buttons|Cart is dynamically updated with unobtrustive, site-wide functionality|PASS|
|Enter shipping details without having a profile, required fields clearly marked as such|Click "checkout" which redirects to a pre-checkout page tailored for an anon user|User can confidently create an order without uncertainty that her order is misplaced or wrongly handled|PASS|
|Select a payment type (card etc) and pay for cart items, with clearly marked breakdown of costs and final billing amount|Clicking "checkout" again and viewing the payment page|Multiple payment options display, pertinent to User's region|PASS|
|Upon successful payment, redirects to success page with order details|Automatic redirect from Stripe payment Javascript|Upon having committed to a purchase, User feels reassured that order is handled properly, having had proper feedback|PASS|
|Receive an email notification that their shipment is being prepared|Check console from the webhook_handler.py file in Invoices (ensure that either Stripe local is listening or you have the correct URL in the Stripe webhook reg page at stripe.com)|User gets further confirmation that their order and payment is properly handled|PASS|

