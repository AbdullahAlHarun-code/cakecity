from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
#from django.db.models import Q
from .models import Product
#from .forms import PostForm
# Create your views here.
def index(request):
    loop_var1 = [1,2,3,4,5,6,7,8]
    loop_var2 = [1,2,3,4,5]
    context = {
        'title':'Test title',
        'loop1':loop_var1,
        'loop2':loop_var2,
    }
    return render(request, 'web/home.html',context)
def shop(request):
    products = Product.objects.all()
    #images = PostImage.objects.filter(post=single_post)
    context = {
        'title':'All Cakes',
        'products':products,
    }
    return render(request, 'products/shop.html',context)
def single_product(request, slug):
    single_post = get_object_or_404(Product, slug=slug)
    context = {
        'title':'',
        'single_product':single_post,
    }
    return render(request, 'products/single.html',context)

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
