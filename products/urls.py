from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.shop, name="category"),
    path('<slug:slug>/', views.single_product, name="single_product"),
    #path('category/', views.shop, name="category"),
]
