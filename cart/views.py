from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

# Create your views here.
def view_cart(request):
    context = {
        'title':'My Cart',
    }
    return render(request, 'cart/cart.html',context)

def add_to_cart(request, item_id):
    quantity = int(request.POST.get('quantuty'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    print(requeset.session['cart'])
    return redirect(redirect_url)
