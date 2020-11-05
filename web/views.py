from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
#from django.db.models import Q
from products.models import Product, CakeCategory, ProductImage, Flavour, Variation, CakeSizeCategory

# This all_category carry the whole products category objects
all_category = CakeCategory.objects.all()

# this function for custome made 404 page view
def error_404_view(request, exception):
    print(request)
    return render(request, '404.html')

# this is home page view 
def index(request):
    featured_cakes = Product.objects.all().filter(featured_cake=True)
    context = {
        'title':'Test title',
        'featured_cakes':featured_cakes,
    }
    return render(request, 'web/home.html',context)
def page(request):
    context = {
        'title':'Test title',
    }
    return render(request, 'web/page.html',context)

def about(request):
    bradcrumb_list = ['about-us']
    context = {
        'title':'About Us',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'web/about-us.html',context)

def cake_flavours(request):
    bradcrumb_list = ['cake-clavours']
    context = {
        'title':'Cake Flavours',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'web/cake-flavours.html',context)

def contacts(request):
    bradcrumb_list = ['contact-us']
    context = {
        'title':'Contact Us',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'web/contact-us.html',context)
def faqs(request):
    bradcrumb_list = ['faqs']
    context = {
        'title':'frequently asked questions',
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'web/faqs.html',context)
