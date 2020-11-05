from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
#from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.conf import settings
from .models import Product, CakeCategory, Variation, Flavour
import json
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
    pagination_path = request.path+'?'
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
        'pagination_path':pagination_path,

    }
    return render(request, 'products/category.html',context)
def index(request):

    context = {
        'title':'Test title',
        'all_category':all_category,
    }
    return render(request, 'web/home.html',context)
def product_pagination(products,page_num):
    p = Paginator(products,3)
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

class Options:
    flavours = Flavour.objects.all()
    slug = None
    id = None
    add_to_cart_press = None
    tier = None
    cake_size_id = 0
    cake_size_name = None
    cake_size_name_array = []
    cake_flavour_id = []
    single_tier_cake_flavour_text = None
    cake_flavour_price_array = []
    quantity = 1
    final_total = 0
    only_cake_price = 0
    only_single_cake_price_flavour = 0
    total_flavour_price = 0

    def get_cake_price(self):
        if self.cake_size_id > 0:
            price = Variation.objects.all().filter(id=self.cake_size_id).first().price
            if price:
                return price
            else:
                return False
    def set_flavour_price_total(self, request):

        if self.cake_size_id > 0:
            price = Variation.objects.all().filter(id=self.cake_size_id).first().price
            if price:
                self.only_cake_price = price
            if self.tier == 1 :
                if len(self.cake_flavour_id) > 0:
                    self.total_flavour_price = self.total_flavour_price + 10
            else:
                if len(self.cake_flavour_id) > 0:
                    for item in self.cake_flavour_id:
                        if(item != 0):
                            flavour_price = Flavour.objects.all().filter(id=item).first().price
                            self.total_flavour_price = self.total_flavour_price + flavour_price


            self.only_single_cake_price_flavour = self.only_cake_price + self.total_flavour_price
            self.final_total = self.only_single_cake_price_flavour*self.quantity


    def set_flavour_data(self, request):
        self.cake_flavour_id.clear()
        if self.cake_size_id > 0:
            if self.tier == 1:
                if 'flavour_variation' in request.POST:
                    flavour_name_value = int(request.POST.get('flavour_variation'))
                    if flavour_name_value>0:
                        self.single_tier_cake_flavour_text = flavour_name_value
                        self.cake_flavour_id.append(flavour_name_value)
                return self.cake_flavour_id
            else:
                variation_select = Variation.objects.all().filter(id=self.cake_size_id)
                self.cake_size_name = variation_select.first().size
                self.cake_size_name_array = self.cake_size_name.split('/')
                for flavour in self.cake_size_name_array:
                    flavour_name = flavour+'_tier_flavour_variation'
                    if flavour_name in request.POST:
                        flavour_name_value = int(request.POST.get(flavour_name))
                        if flavour_name_value>0:
                            self.cake_flavour_id.append(flavour_name_value)
                return self.cake_flavour_id
        else:
            pass


    def is_falvour(self):
        if self.cake_size_id>0:
            return True
    def is_active_addToCart(self):
        if self.tier == len(self.cake_flavour_id):
            return ''
        else:
            return 'disabled'
    def is_active_addToCart_press(self):
        if self.tier == len(self.cake_flavour_id):
            return True
        else:
            return False
    def get_submit_url(self):
        #return reverse('add_to_cart', args=[self.id])
        return "%s/%s" %(settings.SITE_URL, reverse('add_to_cart', args=[self.id]))

def single_product(request, slug):
    add_to_cart_button = 'disabled'
    add_to_cart_press = False
    add_flavour = False
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
    options = Options()
    options.tier = int(single_product.tier)
    options.id = int(single_product.id)
    options.slug = slug
    if request.POST:

        if 'item_quantity' in request.POST:
            print('quantity working')
            options.quantity = int(request.POST.get('item_quantity'))
        if 'add_to_cart_press' in request.POST:
            add_to_cart_press = True
        if 'cake_size' in request.POST:
            cake_size = int(request.POST.get('cake_size'))
            options.cake_size_id = cake_size
            options.set_flavour_data(request)
            options.set_flavour_price_total(request)

    context = {
        'title':'',
        'slug':slug,
        'quantity':request.POST.get('item_quantity'),
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
        #'quantity':quantity,
        'single_quantity_price':single_quantity_price,
        'add_to_cart_press':add_to_cart_press,
        'add_flavour':add_flavour,
        'options':options,
    }
    return render(request, 'products/single.html',context)

def updated_item(request):
    data = json.loads(request.body)
    print(data)
    # quantity = data['quantity']
    # cart = request.session.get('cart', {})
    # if item_id in list(cart.keys()):
    #     cart[item_id] += quantity
    # else:
    #     cart[item_id] = quantity
    # ============================
    # quantity = int(request.POST.get('quantity'))
    # redirect_url = request.POST.get('redirect_url')
    # cart = request.session.get('cart', {})
    # if item_id in list(cart.keys()):
    #     cart[item_id] += quantity
    # else:
    #     cart[item_id] = quantity
    #
    # request.session['cart'] = cart
    # print(request.session['cart'])

    return JsonResponse('Itemhas added', safe=False)
    # data = json.loads(response.body)
    # productId = data['productId']
    # action = data['action']
    # print('Action:', action)
    # print('Product:', productId)

    #return redirect(redirect_url)


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
