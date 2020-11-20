from django.contrib import admin
from .models import Order, OrderItem, OrderItemVariation

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'full_name','city', 'order_total', 'delivery_cost', 'grand_total']
    ordering = ('-date',)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product','quantity', 'item_total']

@admin.register(OrderItemVariation)
class OrderItemVariationAdmin(admin.ModelAdmin):
    list_display = ['order', 'order_item','flavour', 'price']
