from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from products.models import Product, CakeCategory, Variation, Flavour


class Item:
    single_product = None
    cake_size_id = None
    quantity = None
    flavour_name = []
    flavour_name_with_price = []
    flavour_price_array = []
    product_price = 0
    price = 0
    total = 0

    def set_price(self):
        price = self.single_product
        variation_select = Variation.objects.all().filter(id=self.cake_size_id)
        self.product_price = variation_select.first().price
        self.price = self.price + self.product_price
    def set_price_by_flavour(self, flavour_id):
        if int(self.single_product.tier) > 1:
            flavour_price = Flavour.objects.all().filter(id=flavour_id).first().price
            self.price = self.price + flavour_price
            self.flavour_price_array.append(flavour_price)
        if int(self.single_product.tier) == 1:

            self.flavour_price_array.append(10)
            self.price = self.price + 10

    def set_total(self):
        self.total = self.price*int(self.quantity)


    def set_flavour_name(self, flavour_id):
        if int(self.single_product.tier) == 1:
            self.flavour_name.append(str(flavour_id))
            self.flavour_name_with_price.append(str(flavour_id))
        if int(self.single_product.tier) > 1:
            flavour = Flavour.objects.all().filter(id=flavour_id).first()
            self.flavour_name.append(flavour.flavour_name)
            self.flavour_name_with_price.append(flavour.flavour_name+'(€'+str(flavour.price)+')')


def cart_contents(request):
    #del request.session['cart']
    cart_item_count = None
    if 'cart' in request.session:
        cart = request.session['cart']
    else:
        print('test')
        cart = []
    cart_items = []
    sub_total = 0
    grand_total = 0
    delivery_charge_range = 100
    free_delivery_charge = 10
    shipping_charge = 0
    if cart:
        cart_item_count = len(cart)
        for item in cart:
            single_item = Item()
            single_item.single_product = get_object_or_404(Product, pk=item['item_id'])
            single_item.quantity = item['quantity']
            single_item.cake_size_id = item['cake_size_id']
            single_item.set_price()
            if len(item['flavours_id'])>0:
                single_item.flavour_name.clear()
                single_item.flavour_name_with_price.clear()
                single_item.flavour_price_array.clear()
                if int(single_item.single_product.tier) == 1:
                    single_item.set_price_by_flavour(item['flavours_id'])
                    single_item.set_flavour_name(item['flavours_id'])
                else:
                    for item_flavour_id in item['flavours_id']:
                        single_item.set_price_by_flavour(item_flavour_id)
                        single_item.set_flavour_name(item_flavour_id)

            single_item.set_total()
            cart_items.append(single_item)
        for item in cart_items:
            sub_total = sub_total + item.total
        if sub_total > delivery_charge_range:
            grand_total = sub_total + free_delivery_charge
            shipping_charge = free_delivery_charge
        else:
            grand_total = subtotal
    # # cart_items = []
    # total = 1
    # product_count = 0
    # free_delivery = 100
    # delivery = 10
    # grand_total = delivery + total
    context = {
        'cart_item_count':cart_item_count,
        'sub_total':sub_total,
        'grand_total':grand_total,
        'cart_items':cart_items,
    }

    return context
