from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from products.models import Product, Category, Variation, Flavour

# this for view cart page
def view_cart(request):
    context = {
        'title':'My Cart',
    }
    return render(request, 'cart/cart.html',context)
# this is for single product variations
class CakeSizeVariation():
    object = None
    tier_multiple_flavour_id = []
    def get_size_print_name(self):
        return self.object.size
    def get_flavour(self):
        cake_size = self.object.size.split('/')

        if len(cake_size)>0:
            return self.tier_multiple_flavour_id

# this is for add to cart item funtiontionality
def add_to_cart(request, item_id):
    quantity = (request.POST.get('item_quantity'))
    redirect_url = request.POST.get('redirect_url')

    cart = request.session.get('cart')
    item_id = int(item_id)
    cake_size_variation = CakeSizeVariation()
    cake_size_variation.tier_multiple_flavour_id.clear()
    item = None
    if item_id:
        single_product = get_object_or_404(Product, pk=item_id)
        if 'cake_size' in request.POST:
            cake_size_id = int(request.POST.get('cake_size'))
            if cake_size_id>0:
                cake_size = Variation.objects.all().filter(id=cake_size_id)
                cake_size_variation.object = cake_size.first()
                cake_size = cake_size.first().size.split('/')

                if len(cake_size)>0:
                    for flavour in cake_size:
                        flavour_form_name = flavour+'_tier_flavour_variation'

                        if flavour_form_name in request.POST:
                            flavour_id = int(request.POST.get(flavour_form_name))
                            cake_size_variation.tier_multiple_flavour_id.append(flavour_id)

                    item = {
                      "item_id":item_id,
                      "cake_size_id":cake_size_id,
                      "quantity":quantity,
                      "flavours_id":cake_size_variation.get_flavour()
                    };


    if item_id:
        single_product = get_object_or_404(Product, pk=item_id)
        if cart and item:
            cart.append(item)
            messages.success(request, f'Added {single_product.title} to your cart')
        else:
            cart = []
            cart.append(item)
            messages.success(request, f'Added {single_product.title} to your cart')


    request.session['cart'] = cart
    return redirect('cart')

#this is for update cart item change quantity from cart page
def update_cart_item(request, update_item_id):

    if request.POST and update_item_id:
        quantity = (request.POST.get('update_quantity'))
        cart = request.session.get('cart')
        if update_item_id and cart:
            remove_index = int(update_item_id)-1
            cart[remove_index]['quantity'] = quantity
            request.session['cart'] = cart
            messages.warning(request, f'Your item quantity updated to your cart')
    return redirect('cart')

# this is for remove item forom cart page
def remove_item(request, remove_item_id):
    cart = request.session.get('cart')
    if remove_item_id and cart:
        remove_index = int(remove_item_id)-1
        cart.pop(remove_index)
        request.session['cart'] = cart
        messages.warning(request, f'Removed item to your cart')

    return redirect('cart')
