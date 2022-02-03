from django.urls import path
from . import views
urlpatterns = [
    path('', views.view_cart, name="view_cart"),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/create-payment-intent/', views.create_shop_checkout_session, name='create_payment_intent')
]
