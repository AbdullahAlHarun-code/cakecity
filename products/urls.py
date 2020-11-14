from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.all_cakes, name="all_cakes"),
    path('<slug:slug>/', views.single_product, name="single_product"),
    #path('category/<cat:cat>/', views.category, name="category"),
]
