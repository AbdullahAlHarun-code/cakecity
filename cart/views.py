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
