from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopFront.as_view(), name="shop"),
    path('all-shop-customers/', views.AllShopCustomers.as_view(),
         name="all_shop_customers"),
     path('all-shop-orders/', views.AllShopOrders.as_view(), name="all_shop_orders"),
     path('mark-invoice-complete/<str:invoice_order_number>/', views.mark_invoice_complete, name="mark_invoice_complete"),
    path('<int:pk>/', views.ShopItem.as_view(), name="shop_item"),
    path('staff-manage-items/', views.StaffManageItems.as_view(),
         name="staff_manage_items"),
    path('staff-add-item/', views.StaffAddItem.as_view(), name="staff_add_item"),
    path('staff-manage-items/<int:pk>/',
         views.StaffUpdateItem.as_view(), name="staff_update_item"),
    path('staff-delete-item/<int:pk>/',
         views.StaffDeleteItem.as_view(), name="staff_delete_item"),
    path('staff-add-image/', views.StaffAddImage.as_view(), name="staff_add_image"),
    path('update-image/<int:pk>/',
         views.StaffUpdateImage.as_view(), name="update_image"),
     path('add-image-in-product/<int:product_id>/',
         views.add_image_in_product, name="add_image_in_product"),
    path('delete-image-confirm/<int:pk>/',
         views.StaffDeleteImage.as_view(), name="delete_image"),
     path('set-primary-image/<int:product_id>/<int:image_id>/', views.set_primary_image, name='set_primary_image'),
]
