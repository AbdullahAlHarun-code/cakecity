from django.db import models
from products.models import Product, CakeCategory, Variation, Flavour
#from .utils import id_generator
# Create your models here.

# order status options array 
STATUS_CHIOCES = (
    ("Process",'Process'),
    ("Shipment",'Shipment'),
    ("Delivered",'Delivered'),
)
class Order(models.Model):
    order_id = models.CharField(max_length=120, default='ABC')
    sub_total = models.DecimalField
    product_id = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=STATUS_CHIOCES, default='Process')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.order_id
