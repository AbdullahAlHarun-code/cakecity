from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
#from django.db.models import Q
from products.models import Product, ProductImage, Variation, Category, FlavourCategory, Flavour, CakeSizeCategory
from django.contrib.auth.decorators import login_required
# This all_category carry the whole products category objects
all_category = Category.objects.all()

# this function for custome made 404 page view
def error_404_view(request, exception):
    print(request)
    return render(request, '404.html')


# this is home page view
#@login_required(login_url='login')
def index(request):
    featured_cakes = Product.objects.all().filter(featured_cake=True)
    context = {
        'title':'Test title',
        'featured_cakes':featured_cakes,
    }
    return render(request, 'web/home.html',context)



# this is about page view
def about(request):
    bradcrumb_list = ['about-us']
    context = {
        'title':'About Us',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'web/about-us.html',context)

# this is cake-flavour page view
def cake_flavours(request):
    bradcrumb_list = ['cake-clavours']
    context = {
        'title':'Cake Flavours',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'web/cake-flavours.html',context)

# this contact-us page view
def contacts(request):
    bradcrumb_list = ['contact-us']
    context = {
        'title':'Contact Us',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'web/contact-us.html',context)

# this is faqs page view
def faqs(request):
    bradcrumb_list = ['faqs']
    context = {
        'title':'frequently asked questions',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'web/faqs.html',context)
