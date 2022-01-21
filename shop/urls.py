from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopFront.as_view(), name="shop"),
    path('<int:pk>/', views.ShopItem.as_view(), name="shop_item"),
    path('staff-add-item/', views.StaffAddItem.as_view(), name="staff_add_item"),
    path('staff-manage-items/', views.StaffManageItems.as_view(),
         name="staff_manage_items"),
    path('staff-manage-items/<int:pk>/',
         views.StaffUpdateItem.as_view(), name="staff_update_item"),
    path('staff-delete-item/<int:pk>/',
         views.StaffDeleteItem.as_view(), name="staff_delete_item"),
    path('staff-add-image/', views.StaffAddImage.as_view(), name="staff_add_image"),
]
