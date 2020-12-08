from django.contrib import admin
from .models import Customer, BillingAddress, ShippingAddress

# Register Customer admin

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name','email', 'phone', 'date_created']

# Register billing address admin

@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city','eircode', 'updated']

# register shipping address admin

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city','eircode', 'updated']
