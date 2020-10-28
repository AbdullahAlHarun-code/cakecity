from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from .models import Product, CakeCategory
#from .forms import PostForm
# Create your views here.

all_category = CakeCategory.objects.all()
def product_category(request,p_cat):
    category_items = CakeCategory.objects.all().filter(category=p_cat)
    bradcrumb_list = ['cake-shop',p_cat]
    #print(category_items)
    context = {
        'title':category_items[0].get_category_name_by_slug(),
        'category_items':category_items,
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'products/product-category.html',context)
def category(request,cat):
    category_item = get_object_or_404(CakeCategory, category_slug=cat)
    bradcrumb_list = ['cake-shop',cat]
    products = ''
    if category_item is not None:
        #products = get_object_or_404(Product, cake_category=category_item.category_name)
        products = Product.objects.all().filter(cake_category=category_item.category_name)
        paginator_array = product_pagination(products,request.GET.get('page',1))
        products = paginator_array[0]
    context = {
        'title':'Testt title',
        'category_item':category_item,
        'category_slug':cat,
        'products':products,
        'bradcrumb_list':bradcrumb_list,
        'paginator': paginator_array[1],
        'star_loop':range(1,6),
    }
    return render(request, 'products/category.html',context)
def index(request):

    context = {
        'title':'Test title',
        'all_category':all_category,
    }
    return render(request, 'web/home.html',context)
def product_pagination(products,page_num):
    p = Paginator(products,4)
    page_num = page_num
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return [page, p]

def all_cakes(request):
    #images = PostImage.objects.filter(post=single_post)
    query = None
    bradcrumb_list = ['all-cakes']
    products = Product.objects.all()
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                message.error(request, 'You didn\'t enter any search criteria!' )
                return redirect(reverse('all-cakes'))
            queries = Q(title__icontains=query) | Q(description__icontains=query)
            products =products.filter(queries)
    paginator_array = product_pagination(products,request.GET.get('page',1))
    products = paginator_array[0]

    context = {
        'title':'All Cakes',
        'bradcrumb_list':bradcrumb_list,
        'all_category':all_category,
        'paginator': paginator_array[1],
        'products':products,
        'search_term':query,
        'current_path':request.get_full_path(),
    }
    return render(request, 'products/all-cakes.html',context)

def shop(request):
    #images = PostImage.objects.filter(post=single_post)
    bradcrumb_list = ['cake-shop']
    context = {
        'title':'All Cakes Category',
        'bradcrumb_list':bradcrumb_list,
        'all_category':all_category,
    }
    return render(request, 'products/shop.html',context)
def single_product(request, slug):
    single_post = get_object_or_404(Product, slug=slug)
    bradcrumb_list = ['cake-shop',slug]
    context = {
        'title':'',
        'bradcrumb_list':bradcrumb_list,
        'single_product':single_post,
        'star_loop':range(1,6),
    }
    return render(request, 'products/single.html',context)
def updated_item(response):
    #return JsonResponse('Itemhas added', safe=False)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
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
