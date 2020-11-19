from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.forms import ShippingAddressForm
from accounts.models import ShippingAddress

# Create your views here.


def checkout(request):
    is_login = request.user.is_authenticated
    edit_action = False
    if is_login == False:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Username or password is incorrect!')
                return redirect('login')

    if is_login:
        try:
            shipping_address = ShippingAddress.objects.all().first()
        except:
            shipping_address = None

        if 'edit' in request.GET:
            address = request.GET.get('edit')
            if address == 'shipping-address':
                edit_action = True




        shipping_address_form = ShippingAddressForm(instance=shipping_address)
    context = {
        'title':'Checkout Page',
        'is_login':is_login,
        'shipping_address_form':shipping_address_form,
        'shipping_address':shipping_address,
        'edit_action':edit_action,
    }
    return render(request, 'checkout/checkout.html',context)
