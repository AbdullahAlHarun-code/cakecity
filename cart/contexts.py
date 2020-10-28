from decimal import Decimal
from django.conf import settings

def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    free_delivery = 100
    delivery = 10
    grand_total = delivery + total

    context = {
        'cart_items':cart_items,
        'total':total,
        'product_count':product_count,
        'delivery':delivery,
        'free_delivery':free_delivery,
        'grand_total':grand_total,
    }

    return context
