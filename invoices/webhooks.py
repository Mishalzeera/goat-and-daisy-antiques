from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .webhook_handler import StripeWebhookHandlerSHOP, StripeWebhookHandlerWORKSHOP
import stripe


@require_POST
@csrf_exempt
def shop_webhook(request):
    """
    Takes webhooks from the Stripe API and sends it to the classes in webhook_handler.py.
    """
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # From the webhook metadata we created in the payment intent. See .views
    session = event['data']['object']
    session_metadata = session['metadata']
    service_type = session_metadata.shop_or_workshop
    order_number = session_metadata.unique_order_number
    customer_email = session_metadata.customer_email
    # ...after checking which type of transaction
    if service_type == "Workshop":

        invoice_type = session_metadata.invoice_type
        handler = StripeWebhookHandlerWORKSHOP(
            request, order_number, invoice_type, customer_email)

    elif service_type == "Shop":
        # Get the shopping cart from the metadata in string format
        meta_cart = session_metadata.shopping_cart

        # Create an list using the white spaces as delimiter
        string_cart = meta_cart.split(" ")
        # Getting the whitespaces out by filtering out None values
        no_none_cart = [*filter(None, string_cart)]
        # Converting the result into integers for the handler
        shopping_cart = [int(item) for item in no_none_cart]

        # Send all of this to the handler class

        handler = StripeWebhookHandlerSHOP(
            request, order_number, shopping_cart, customer_email)

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_suceeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']

    event_handler = event_map.get(event_type)

    response = event_handler(event)
    return response
