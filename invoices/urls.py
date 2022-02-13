from django.urls import path
from . import views
from .webhooks import shop_webhook

urlpatterns = [
    path('cart/', views.view_cart, name="view_cart"),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('confirm-details/', views.precheckout, name="precheckout"),
    path('checkout/', views.checkout, name='checkout'),
    path('workshop-checkout/<int:invoice_id>/', views.workshop_checkout, name='workshop_checkout'),
    path('checkout/create-payment-intent/', views.create_checkout_session, name='create_payment_intent'),
    path('success/', views.success, name="success"),
    path('wh/', shop_webhook, name="webhook"),
]
