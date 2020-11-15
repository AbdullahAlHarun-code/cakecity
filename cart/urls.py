from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.view_cart, name="cart"),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_item/<int:remove_item_id>/', views.remove_item, name="remove_item"),
    path('update_cart_item/<int:update_item_id>/', views.update_cart_item, name="update_cart_item"),
]
