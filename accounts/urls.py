from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.loginPage, name="account"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('profile/', views.profile, name="profile"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('order-history/', views.order_history, name="order_history"),
    path('order/<slug:order_id>/', views.order, name="single_order"),
    path('change-password/',views.change_password, name="change_password"),
    path('address/',views.address, name="address"),
]
