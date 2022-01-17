from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopFront.as_view(), name="shop"),
    path('shop-item/<int:pk>/', views.ShopItem.as_view(), name="shop_item"),
]