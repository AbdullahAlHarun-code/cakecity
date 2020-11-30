from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from products.models import Product, Category, Flavour, Variation, Flavour, FlavourCategory


class Item:
    single_product = None
    cake_size_id = None
    quantity = None
    flavour_objects_array = []
    product_price = 0
    price = 0
    total = 0

    def set_price(self):
        variation_select = Variation.objects.all().filter(id=self.cake_size_id)
        self.product_price = variation_select.first().price
        self.price = self.product_price

    def set_total(self):
        flavour_price_total = 0
        for flavour in self.flavour_objects_array:
            flavour_price_total = flavour_price_total + flavour.price
        self.price = self.price + flavour_price_total
        self.total = self.price*int(self.quantity)



def cart_contents(request):
    #del request.session['cart']
    cart_item_count = None
    if 'cart' in request.session:
        cart = request.session['cart']
    else:
        cart = []

    cart_items = []
    sub_total = 0
    grand_total = 0
    delivery_charge_range = 800
    delivery_charge = 10
    shipping_charge = 0

    if cart:
        cart_item_count = len(cart)
        for item in cart:
            single_item = Item()
            flavour_objects_array = []
            single_item.single_product = get_object_or_404(Product, pk=item['item_id'])
            single_item.quantity = item['quantity']
            single_item.cake_size_id = item['cake_size_id']
            single_item.set_price()
            if len(item['flavours_id'])>0:
                for item_flavour_id in item['flavours_id']:
                    flavour = Flavour.objects.all().filter(id=item_flavour_id).first()
                    flavour_objects_array.append(flavour)


            single_item.flavour_objects_array = flavour_objects_array
            single_item.set_total()
            cart_items.append(single_item)

        for item in cart_items:
            sub_total = sub_total + item.total
        if sub_total < delivery_charge_range:
            grand_total = sub_total + delivery_charge
            shipping_charge = delivery_charge
        else:
            grand_total = sub_total
            shipping_charge = 0

    context = {
        'cart_item_count':cart_item_count,
        'sub_total':sub_total,
        'grand_total':grand_total,
        'cart_items':cart_items,
        'shipping_charge':shipping_charge,
    }

    return context
