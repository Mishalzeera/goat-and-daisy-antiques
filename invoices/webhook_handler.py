from django.http import HttpResponse

class StripeWebhookHandlerSHOP:

    def __init__(self, request):
        self.request = request 

    def handle_event(self, event):
        print("CLASS_UNKNOWN")
        return HttpResponse(
            content = f'Unhandled Webhook received {event["type"]}',
            status = 200
            )
        
    def handle_payment_intent_suceeded(self, event):
        print("CLASS_SUCCEEDED")
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

    def handle_payment_intent_payment_failed(self, event):
        print("CLASS_FAILED")
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

class StripeWebhookHandlerWORKSHOP:

    def __init__(self, request):
        self.request = request 

    def handle_event(self, event):
        print("CLASS_UNKNOWN_WORKSHOP")
        return HttpResponse(
            content = f'Unhandled Webhook received {event["type"]}',
            status = 200
            )
        
    def handle_payment_intent_suceeded(self, event):
        print("CLASS_SUCCEEDED_WORKSHOP")
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

    def handle_payment_intent_payment_failed(self, event):
        print("CLASS_FAILED_WORKSHOP")
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )
    
    
