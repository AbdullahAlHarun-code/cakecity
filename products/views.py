from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from .models import Product, CakeCategory, Variation, Flavour
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
    #print(request.path().objects.filter(global_url__id=1).all())
    query = None
    sort = None
    bradcrumb_list = ['all-cakes']
    products = Product.objects.all()
    count_all_products = products.count()
    pagination_path = request.path+'?'
    print(pagination_path)
    if request.GET:
        if 'order_by' in request.GET:
            sortkey = request.GET['order_by']
            sort = sortkey
            if 'page' not in request.GET:
                if sortkey =='title':
                    products = products.order_by('title')
                if sortkey =='rating':
                    products = products.order_by('-rating')
                if sortkey =='latest':
                    products = products.order_by('create_date')
                if sortkey =='low-to-high':
                    products = products.order_by('price')
                if sortkey =='high-to-low':
                    products = products.order_by('-price')

            pagination_path = request.path+'?order_by='+sortkey+'&'

            #print(request.GET['page'])
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
        'star_loop':range(1,6),
        'pagination_path':pagination_path,
        'count_all_products':count_all_products,
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
    add_to_cart_button = 'disabled'
    cake_size= 0
    total= 0
    single_quantity_price = 0
    quantity = 1
    select_size_price = None
    select_size_array = None
    flavour_variation = 0
    flavours = None
    tier_flavour_variation = []
    single_product = get_object_or_404(Product, slug=slug)
    bradcrumb_list = ['cake-shop',slug]
    if request.POST:

        if 'cake_size' in request.POST:
            cake_size = int(request.POST.get('cake_size'))
            if cake_size>1:
                add_to_cart_button = ''
        if int(single_product.tier)>1 and cake_size>0:
            variation_select = Variation.objects.all().filter(id=cake_size)
            select_size_array = variation_select.first().size.split('/')
            for flavour in select_size_array:
                flavour_name = flavour+'_tier_flavour_variation'
                flavours = Flavour.objects.all()
                if flavour_name in request.POST:
                    flavour_name_value = int(request.POST.get(flavour_name))
                    tier_flavour_variation.append(flavour_name_value)
            if 0 in tier_flavour_variation:
                add_to_cart_button = 'disabled'

        else:
            if 'flavour_variation' in request.POST:
                flavour_variation = int(request.POST.get('flavour_variation'))

    if cake_size>0:
        variation_select = Variation.objects.all().filter(id=cake_size)
        select_size_price = variation_select.first().price
        total = total+select_size_price
        single_quantity_price = total
    if flavour_variation>0:
        total = total+10
    if len(tier_flavour_variation)>0:
        for item in tier_flavour_variation:
            print(item)
            if(item != 0):
                total = total+Flavour.objects.all().filter(id=item).first().price
                single_quantity_price = single_quantity_price + Flavour.objects.all().filter(id=item).first().price
    if request.POST:
        if 'quantity' in request.POST:
            quantity = int(request.POST.get('quantity'))
            if quantity > 0:
                print(quantity)
                print(total)
                total = total*int(quantity)
            else:
                add_to_cart_button = 'disabled'

    context = {
        'title':'',
        'bradcrumb_list':bradcrumb_list,
        'single_product':single_product,
        'star_loop':range(1,6),
        'cake_size':int(cake_size),
        'flavour_variation':int(flavour_variation),
        'tier_flavour_variation':tier_flavour_variation,
        'select_size_price':select_size_price,
        'total':total,
        'flavours':flavours,
        'select_size_array':select_size_array,
        'add_to_cart_button':add_to_cart_button,
        'quantity':quantity,
        'single_quantity_price':single_quantity_price,
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

# 0861564183
# bellalmiah1964@gmail.com
# Bellal Miah
# Urgent Account Recovery
#
# I have an account with mygov
# Details:
# Name: Bellal Miah
# PPSN: 4307152S
# DOB: 01/01/1964
# Mobile: 0861564183
# But when I try to login revenue site, by mistake I really for a new account.
# And therefore my mygov account now block
# I try to fix forgotten password but its is not working
# Please advise me how I fix this issue
# It is too urgent for me
# Thanks

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
