from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.user.username:
            return self.user.username
        else:
            return ''

class BillingAddress(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=200, null=True)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    address_line_3 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    eircode = models.CharField(max_length=200, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=200, null=True)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    address_line_3 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    eircode = models.CharField(max_length=200, null=True)
    updated = models.DateTimeField(auto_now_add=True)
