from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from products.models import Product, Category, ProductImage, Flavour, Variation, Flavour, FlavourCategory
from checkout.models import Order, OrderItem, OrderItemVariation


class Item:
    product = None
    product_image = None
    size = None
    flavour = []
    unit_price = 0
    quantity = 0
    total = 0

def get_all_order(request):
    all_order_list = []
    all_orders = Order.objects.all().filter(username=request.user.username).order_by('-date')
    for order in all_orders:
        order = get_order(order.order_id)
        all_order_list.append(order)
    return all_order_list
def get_order(order_id):
    order_items_array = []

    order = get_object_or_404(Order, order_id=order_id)
    order_items = OrderItem.objects.all().filter(order=order)

    for item in order_items:
        order_items_flavour = []
        single_item = Item()
        single_item.product = item.product
        single_item.product_image = ProductImage.objects.all().filter(product=item.product).first().image
        single_item.quantity = item.quantity
        single_item.total = item.item_total
        single_item.size = item.size
        single_item.unit_price = item.product_price
        item_variations = OrderItemVariation.objects.all().filter(order_item=item,order=order)

        #product = Product.objects.get(id=items.product.id)
        for variation in item_variations:
            flavour = Flavour.objects.get(id=variation.flavour.id)
            order_items_flavour.append(flavour)
        single_item.flavour = order_items_flavour
        order_items_array.append(single_item)




    context = {
        'order_items':order_items_array,
        'order':order,
    }

    return context
