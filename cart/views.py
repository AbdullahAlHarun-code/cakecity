from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from products.models import Product, CakeCategory, Variation, Flavour

# Create your views here.
def view_cart(request):
    context = {
        'title':'My Cart',
    }
    #request.session['cart']=[]
    print('cart', request.session['cart'])
    return render(request, 'cart/cart.html',context)
class CakeSizeVariation():
    object = None
    tier_one_flavour_id = None
    tier_multiple_flavour_id = []
    def get_size_print_name(self):
        return self.object.size
    def get_flavour(self):
        cake_size = self.object.size.split('/')
        if len(cake_size)==1:
            if self.tier_one_flavour_id==1:
                return 'Gold(€10)'
            if self.tier_one_flavour_id==2:
                return 'Silver(€10)'
            if self.tier_one_flavour_id==3:
                return 'Rose Gold(€10)'
        if len(cake_size)>1:
            return self.tier_multiple_flavour_id

def add_to_cart(request, item_id):
    print('quantity yes: ',request.POST.get('redirect_url'))
    quantity = (request.POST.get('item_quantity'))
    redirect_url = request.POST.get('redirect_url')

    cart = request.session.get('cart')
    item_id = int(item_id)
    cake_size_variation = CakeSizeVariation()
    item = None
    if item_id:
        single_product = get_object_or_404(Product, pk=item_id)
        if 'cake_size' in request.POST:
            cake_size_id = int(request.POST.get('cake_size'))
            if cake_size_id>0:
                cake_size = Variation.objects.all().filter(id=cake_size_id)
                cake_size_variation.object = cake_size.first()
                cake_size = cake_size.first().size.split('/')
                if len(cake_size)==1:
                    cake_size_variation.tier_one_flavour_id = int(request.POST.get('flavour_variation'))
                    item = {
                      "item_id":item_id,
                      "cake_size_id":cake_size_id,
                      "quantity":quantity,
                      "flavours_id":cake_size_variation.get_flavour()
                    };
                if len(cake_size)>1:
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
    print('cart', request.session['cart'])
    #print('Tier',single_product.tier)
    return redirect('cart')
def remove_item(request, remove_item_id):
    quantity = (request.POST.get('quantity'))
    #redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart')
    if remove_item_id and cart:
        remove_index = int(remove_item_id)-1
        cart.pop(remove_index)
        request.session['cart'] = cart
        print(request.session['cart'])
        print('remove_index',remove_index)
    # if remove_item_id in list(cart.keys()):
    #     cart.remove(remove_item_id)



    return redirect('cart')
