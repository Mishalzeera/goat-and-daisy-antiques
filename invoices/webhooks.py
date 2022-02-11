from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .webhook_handler import StripeWebhookHandlerSHOP, StripeWebhookHandlerWORKSHOP
import stripe


@require_POST
@csrf_exempt
def shop_webhook(request):
    
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    endpoint_secret = settings.LOCAL_STRIPE_WH_SECRET
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


    # From the webhook metadata, we first get a more handy place to start
    session = event['data']['object']
    session_metadata = session['metadata']
    service_type = session_metadata.shop_or_workshop
    
    if service_type == "Workshop":      
        handler = StripeWebhookHandlerWORKSHOP(request)
    elif service_type == "Shop":
        handler = StripeWebhookHandlerSHOP(request)
    
    

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_suceeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)
    
    response = event_handler(event)
    print(response)
    return response 


@require_POST
@csrf_exempt
def workshop_webhook(request):
    
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    endpoint_secret = settings.LOCAL_STRIPE_WH_SECRET
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
    
    handler = StripeWebhookHandlerWORKSHOP(request)

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_suceeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)
    
    response = event_handler(event)
    print(response)
    return response 