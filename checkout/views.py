from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .forms import UserRegisterForm
# Create your views here.

def login(request):
    context = {
        'title':'Login',
    }
    return render(request, 'accounts/login.html',context)

def register(request):
    context = {
        'title':'Register',
        'form':UserRegisterForm()
    }
    return render(request, 'accounts/register.html',context)

def checkout(request):
    pass
