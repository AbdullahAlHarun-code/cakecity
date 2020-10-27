from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
#from django.db.models import Q
from products.models import Product, CakeCategory, ProductImage, Flavour, Variation, CakeSizeCategory
#from .forms import PostForm
# Create your views here.

all_category = CakeCategory.objects.all()
loop1 = [1,2,3,4,5,6]
loop2 = [1,2,3,4,5,6]
def error_404_view(request, exception):
    print(request)
    return render(request, '404.html')
def index(request):
    context = {
        'title':'Test title',
        'loop1':loop1,
        'loop2':loop2
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
# def post_create(response):
#     return HttpResponse("<h1>Ad New post</h1>")


# def all_posts(request):
#     posts = Post.objects.all()
#     query = None
#     if request.GET:
#
#         if 'q' in request.GET:
#             query = request.GET['q']
#             print(request.GET)
#             if not query:
#                 messages.error(request, 'You didn\'t enter any post name!')
#                 return redirect(reverse('allposts'))
#             queries = Q(title__icontains=query) | Q(content__icontains=query)
#             posts = posts.filter(queries)
#
#
#     context = {
#         'posts':posts,
#         'search_term':query
#     }
#     return render(request, 'posts/index.html',context)
#
# def post_details(request,post_id):
#     single_post = get_object_or_404(Post, id=post_id)
#     images = PostImage.objects.filter(post=single_post)
#     context = {
#         'post':single_post,
#         'images':images
#     }
#     return render(request, 'posts/view.html',context)
#
# def create_post(request):
#     form = PostForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         messages.success(request, 'Successfully Created')
#         return redirect('home')
#     #form = PostForm()
#     context = {
#         'form':form
#     }
#     return render(request, 'posts/post_form.html',context)
#
# def post_update(request, post_id=None):
#     single_post = get_object_or_404(Post, id=post_id)
#     form = PostForm(request.POST or None, instance=single_post)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         messages.success(request, 'Successfully updated')
#         return HttpResponseRedirect(instance.get_absolute_url())
#     context = {
#         'title':single_post.title,
#         'single_post':single_post,
#         'form':form
#     }
#     return render(request, 'posts/post_form.html',context)
#
# def delete_update(request, post_id=None):
#     single_post = get_object_or_404(Post, id=post_id)
#     single_post.delete()
#     messages.success(request, 'Successfully deleted')
#     return redirect('allposts')
