from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopFront.as_view(), name="shop")
]