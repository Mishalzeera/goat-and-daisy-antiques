from django.urls import path
from . import views
urlpatterns = [
    path('cart/', views.view_cart, name="view_cart"),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.checkout, name='checkout'),
    path('workshop-checkout/<int:invoice_id>/', views.workshop_checkout, name='workshop_checkout'),
    path('checkout/create-payment-intent/', views.create_shop_checkout_session, name='create_payment_intent')
]
