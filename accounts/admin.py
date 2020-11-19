from django.contrib import admin
from .models import Customer, BillingAddress, ShippingAddress
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name','email', 'phone', 'date_created']

@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city','eircode', 'updated']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city','eircode', 'updated']
