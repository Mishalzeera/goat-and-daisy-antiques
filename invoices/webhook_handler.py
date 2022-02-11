from django.http import HttpResponse

class StripeWebhookHandlerSHOP:

    def __init__(self, request):
        self.request = request 

    def handle_event(self, event):
        print("THIS IS AN UNKNOWN SHOP ORDER")
        return HttpResponse(
            content = f'Unhandled Webhook received {event["type"]}',
            status = 200
            )
        
    def handle_payment_intent_suceeded(self, event):
        print("THIS IS A SUCCESSFUL SHOP ORDER")
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

    def handle_payment_intent_payment_failed(self, event):
        print("THIS IS A FAILED WORKSHOP ORDER")
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

class StripeWebhookHandlerWORKSHOP:

    def __init__(self, request):
        self.request = request 

    def handle_event(self, event):
        print("THIS IS AN UNKNOWN_WORKSHOP ORDER")
        return HttpResponse(
            content = f'Unhandled Webhook received {event["type"]}',
            status = 200
            )
        
    def handle_payment_intent_suceeded(self, event):
        print("THIS IS A SUCCESSFUL WORKSHOP ORDER")
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )

    def handle_payment_intent_payment_failed(self, event):
        print("THIS IS An UNSUCCESSFUL WORKSHOP ORDER")
        return HttpResponse(
            content = f'Webhook received {event["type"]}',
            status = 200
            )
    
    
