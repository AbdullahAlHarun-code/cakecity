from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import BaseUserManager
from accounts.forms import ShippingAddressForm, UserRegisterForm
from accounts.models import ShippingAddress, Customer
from .forms import OrderForm
from .models import Order
from cart.contexts import cart_contents

import stripe
# Create your views here.


def checkout(request):
    is_login = request.user.is_authenticated
    edit_action = False

    if request.method == 'POST':
        if 'edit' not in request.GET:
            # initial orderForm post data
            form_data = {
                'full_name':request.POST['full_name'],
                'email':request.POST['email'],
                'phone_number':request.POST['phone_number'],
            }
            order_form = OrderForm(form_data)
            # check choose save_info in profile
            try:
                save_info = request.POST['save_info']
            except:
                save_info = False

        if is_login == False:
            # if press login
            if 'login' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, 'You are successfully logged in!')
                    return redirect('checkout')
                else:
                    messages.error(request, 'Username or password is incorrect!')
                    return redirect('checkout')
            else:
                # if press complete button
                if 'edit' not in request.GET:
                    # check choose create account
                    try:
                        create_account = request.POST['save_info']
                    except:
                        create_account = False

                    # initial shipping address form post data
                    shipping_address_form = ShippingAddressForm(request.POST)

                    register_data = {
                        'username':(request.POST['full_name'].split())[-1],
                        'email':request.POST['email'],
                        'password1':password,
                        'password2':password,
                    }
                    # initial register form with register data
                    register_form = UserRegisterForm(register_data)
                    if register_form.is_valid() and shipping_address_form.is_valid() and order_form.is_valid():
                        # if create_account true
                        if create_account:
                            # generate unique auto password
                            password = BaseUserManager().make_random_password()
                            # create new user
                            user = register_form.save()
                            #create new customer
                            Customer.objects.create(user=user,email=email,name=request.POST['full_name'],phone=request.POST['phone_number'])

                            # auto login
                            new_user = authenticate(username=username,password=password)
                            login(request, new_user)
                            # save shipping details
                            if save_info:
                                instance_shipping = shipping_address_form.save(commit=False)
                                if request.user.id:
                                    instance_shipping.user = request.user
                                    instance_shipping.save()


                        # create new order
                        Order.objects.create(
                            full_name=request.POST['full_name'],
                            email=request.POST['email'],
                            phone_number=request.POST['phone_number'],
                            address_line_1=request.POST['address_line_1'],
                            address_line_2=request.POST['address_line_2'],
                            address_line_3=request.POST['address_line_3'],
                            city=request.POST['city'],
                            eircode=request.POST['eircode'],
                            delivery_cost=10,
                            order_total=10,
                            grand_total=10
                        )

                        # thanks message and redirect
                        messages.success(request, f'Account was created for {username}!You are now logged in.')
                        # redirect success page
                        return redirect('success')
                    else:
                        print('not form valid')
        # if user already login
        if is_login:
            # get user shipping address
            try:
                shipping_address = ShippingAddress.objects.all().filter(user=request.user).first()
            except:
                shipping_address = None
            # initial shipping address form data
            shipping_address_form = ShippingAddressForm(instance=shipping_address)
            # edit shipping address
            if 'edit' in request.GET:
                if shipping_address is not None:
                    shipping_address_form = ShippingAddressForm(request.POST,instance=shipping_address)
                else:
                    shipping_address_form = ShippingAddressForm(request.POST)

                if shipping_address_form.is_valid():

                    shipping_address_form.user = request.user
                    instance_shipping = shipping_address_form.save()
                    messages.success(request,'Your shipping address successfully updated!')
                    return redirect('checkout')
            else:
                # if user login and press complete order
                # if order form valid
                if order_form.is_valid():

                    if shipping_address:
                        # if shipping address have
                        # create new order
                        Order.objects.create(
                            full_name=request.POST['full_name'],
                            email=request.POST['email'],
                            phone_number=request.POST['phone_number'],
                            address_line_1=shipping_address.address_line_1,
                            address_line_2=shipping_address.address_line_2 if shipping_address.address_line_2 else '',
                            address_line_3=shipping_address.address_line_3 if shipping_address.address_line_3 else '',
                            city=shipping_address.city,
                            eircode=shipping_address.eircode,
                            delivery_cost=10,
                            order_total=10,
                            grand_total=10
                        )
                    else:
                        # if shipping address do not have
                        # initial order form data already done in top
                        # initial shipping address form data
                        shipping_address_form = ShippingAddressForm(request.POST)
                        # validation for order form and shipping address form
                        if shipping_address_form.is_valid():
                            if save_info:
                                instance_shipping = shipping_address_form.save(commit=False)
                                if request.user.id:
                                    instance_shipping.user = request.user
                                    instance_shipping.save()

                            # create new order
                            Order.objects.create(
                                full_name=request.POST['full_name'],
                                email=request.POST['email'],
                                phone_number=request.POST['phone_number'],
                                address_line_1=request.POST['address_line_1'],
                                address_line_2=request.POST['address_line_2'],
                                address_line_3=request.POST['address_line_3'],
                                city=request.POST['city'],
                                eircode=request.POST['eircode'],
                                delivery_cost=10,
                                order_total=10,
                                grand_total=10
                            )

    else:
        if 'edit' in request.GET:
            edit_action = True
        # if not post and login
        if is_login:
            # get user shipping address
            try:
                shipping_address = ShippingAddress.objects.all().filter(user=request.user).first()
            except:
                shipping_address = None
            # shipping address form
            shipping_address_form = ShippingAddressForm(instance=shipping_address)
        else:
            # if not post and not login
            # shipping address form
            shipping_address_form = ShippingAddressForm()
            shipping_address = None

        #print
        #print('grand total', grand_total)

    # Stripe set up and integrations
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    total = 25
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount = stripe_total,
        currency = settings.STRIPE_CURRENCY,
    )



    if not stripe_public_key:
        message.warning(request,'Stripe puclic key is missing. Did you forget to set it your environment?')
    context = {
        'title':'Checkout',
        'is_login':is_login,
        'shipping_address_form':shipping_address_form,
        'shipping_address':shipping_address,
        'edit_action':edit_action,
        'OrderForm':OrderForm(),
        'stripe_public_key':stripe_public_key,
        'client_secret':intent.client_secret,
    }
    return render(request, 'checkout/checkout.html',context)

def success(request):

    context = {
        'title':'Success',

    }
    return render(request, 'checkout/success.html',context)
