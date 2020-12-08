import uuid
from django.db import models
from django.contrib.auth.models import User
from django import forms
from products.models import Product, Flavour
from django.db.models import Sum
from django.conf import settings


class Order(models.Model):
    order_id        = models.CharField(max_length=32, null=False, editable=False)
    username        = models.CharField(max_length=254, null=False, blank=False)
    full_name       = models.CharField(max_length=50, null=False, blank=False)
    email           = models.EmailField(max_length=254, null=False, blank=False)
    phone_number    = models.CharField(max_length=20, null=False, blank=True)
    address_line_1  = models.CharField(max_length=80, null=False, blank=False)
    address_line_2  = models.CharField(max_length=80, null=False, blank=True)
    address_line_3  = models.CharField(max_length=80, null=False, blank=True)
    city            = models.CharField(max_length=40, null=False, blank=False)
    eircode         = models.CharField(max_length=20, null=False, blank=False)
    date            = models.DateTimeField(auto_now_add=True)
    delivery_cost   = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total     = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total     = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)

    def _generate_order_id(self):
        # generate a random unique number
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self._generate_order_id()
        super().save(*args, **kwargs)
    def update_total(self):
        self.order_total = self.lineitems.aggregate(Sum('item_total'))['item_total__sum']
        self.save()

    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order       = models.ForeignKey(Order, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product     = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE)
    size       = models.CharField(max_length=50, null=False, blank=False)
    quantity    = models.IntegerField(null=False, blank=False, default=0)
    product_price  = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    item_total  = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)


    def __str__(self):
        return self.product.title

class OrderItemVariation(models.Model):
    order       = models.ForeignKey(Order, blank=False, on_delete=models.CASCADE)
    order_item  = models.ForeignKey(OrderItem, blank=False, on_delete=models.CASCADE)
    flavour     = models.ForeignKey(Flavour, blank=False, on_delete=models.CASCADE)
    price       = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)


    def __str__(self):
        return self.flavour.flavour_name
