from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, CustomerForm, CustomerChangePassword
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .models import Customer, BillingAddress, ShippingAddress
from .forms import  BillingAddressForm, ShippingAddressForm
from django.contrib.auth import update_session_auth_hash
# Create your views here.
@unauthenticated_user
def loginPage(request):

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
    context = {
        'title':'Login',
    }
    return render(request, 'accounts/login.html',context)

@unauthenticated_user
def registerPage(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            #create new customer
            Customer.objects.create(user=user, email=email)
            messages.success(request, f'Account was created for {username}!')
            return redirect('login')
        else:
            messages.error(request, form.errors)
    context = {
        'title':'Register',
        'form':form
    }
    return render(request, 'accounts/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    customer = Customer.objects.all().filter(user=request.user).first()
    form = CustomerForm(instance = customer)
    context = {
        'title':'My Profile',
        'customer':customer,
        'form':form,
        'active':'profile'
    }
    return render(request, 'accounts/profile.html',context)

@login_required(login_url='login')
def edit_profile(request):
    customer = Customer.objects.all().filter(user=request.user).first()
    form = CustomerForm(instance = customer)

    if request.method == 'POST':
        f = CustomerForm(request.POST, instance=customer)

        if f.is_valid:
            new = f.save()
            print(new)
            username = request.user
            messages.success(request, f'Account Information was saved for {username}!')
            return redirect('profile')

    customer = Customer.objects.all().filter(user=request.user).first()
    context = {
        'title':'My Profile',
        'customer':customer,
        'form':form,
        'active':'profile'
    }
    return render(request, 'accounts/edit-profile.html',context)


@login_required(login_url='login')
def order_history(request):
    orders = None
    context = {
        'title':'View All Orders',
        'orders':orders,
        'active':'order-history'
    }
    return render(request, 'accounts/orders.html',context)

@login_required(login_url='login')
def address(request):
    billing_address_form = BillingAddressForm()
    shipping_address_form = ShippingAddressForm()

    try:
        billing_address = BillingAddress.objects.filter(user=request.user).first()
    except:
        billing_address = None
    try:
        shipping_address = ShippingAddress.objects.all().first()
    except:
        shipping_address = None

    is_billing_address = False
    is_shipping_address = False
    action = None
    if request.method == 'GET':
        if 'add' in request.GET:
            address = request.GET.get('add')
            if address == 'billing-address':
                if billing_address:
                    return redirect('/accounts/address'+'/?edit=billing-address')
                action = 'add'
                is_billing_address = True
            if address == 'shipping-address':
                if shipping_address:
                    return redirect('/accounts/address'+'/?edit=shipping-address')
                action = 'add'
                is_shipping_address = True
        if 'edit' in request.GET:
            action = 'edit'
            address = request.GET.get('edit')
            if address == 'billing-address':
                if billing_address:
                    billing_address_form = BillingAddressForm(instance=billing_address)
                else:
                    return redirect('/accounts/address'+'/?add=billing-address')
                is_billing_address = True

            if address == 'shipping-address':
                if shipping_address:
                    shipping_address_form = ShippingAddressForm(instance=shipping_address)
                else:
                    return redirect('/accounts/address'+'/?add=shipping-address')
                is_shipping_address = True





    if request.method == 'POST':
        if billing_address is not None:
            billing_address_form = BillingAddressForm(request.POST,instance=billing_address)
        else:
            billing_address_form = BillingAddressForm(request.POST)

        if shipping_address is not None:
            shipping_address_form = ShippingAddressForm(request.POST,instance=shipping_address)
        else:
            shipping_address_form = ShippingAddressForm(request.POST)
        if 'add_billing' in request.POST or 'edit_billing' in request.POST:
            print('billing address')
            if billing_address_form.is_valid():
                print('yes billing')
                billing_address_form.user=int(request.user.id)
                instance_billing = billing_address_form.save(commit=False)
                instance_billing.user = request.user
                instance_billing.save()
                messages.success(request, 'Your billing address had successfully added!' )
                return redirect('address')
        if 'add_shipping' in request.POST or 'edit_shipping' in request.POST:
            print('shipping address')
            if shipping_address_form.is_valid():
                print('yes shipping')
                shipping_address_form.user=int(request.user.id)
                instance_shipping = shipping_address_form.save(commit=False)
                instance_shipping.user = request.user
                instance_shipping.save()
                messages.success(request, 'Your shipping address had successfully added!' )
                return redirect('address')


    context = {
        'title':'Address',
        'billing_address_form':billing_address_form,
        'shipping_address_form':shipping_address_form,
        'billing_address':billing_address,
        'shipping_address':shipping_address,
        'active':'address',
        'action':action,
        'is_billing_address':is_billing_address,
        'is_shipping_address':is_shipping_address,
    }
    return render(request, 'accounts/address.html',context)


@login_required(login_url='login')
def change_password(request):

    if request.method == 'POST':
        form = CustomerChangePassword(data=request.POST, user=request.user)
        if form.is_valid():
            print('yes')
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            print('no')
            return redirect('change_password')
    else:
        print('not submit')
        form = CustomerChangePassword(user=request.user)

    context = {
        'title':'Change Password',
        'form':form,
        'active':'change-password'
    }
    return render(request, 'accounts/change-password.html',context)
