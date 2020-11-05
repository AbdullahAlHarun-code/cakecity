import time
from django.shortcuts import render, redirect, reverse
from products.models import Product, CakeCategory, Variation, Flavour
# Create your views here.

def checkout(request):
    bradcrumb_list = ['cart','checkout']
    context = {
        'title':'Checkout Page',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'orders/checkout.html',context)
