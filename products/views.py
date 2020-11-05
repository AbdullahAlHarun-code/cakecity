from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.conf import settings
from .models import Product, CakeCategory, Variation, Flavour
import json

# this is for all products category variable
all_category = CakeCategory.objects.all()

#  this is for all product category page view
def product_category(request,p_cat):
    category_items = CakeCategory.objects.all().filter(category=p_cat)
    bradcrumb_list = ['cake-shop',p_cat]
    context = {
        'title':category_items[0].get_category_name_by_slug(),
        'category_items':category_items,
        'bradcrumb_list':bradcrumb_list,
    }
    return render(request, 'products/product-category.html',context)

# this is for single category page view
def category(request,cat):
    category_item = get_object_or_404(CakeCategory, category_slug=cat)
    bradcrumb_list = ['cake-shop',cat]
    products = ''
    pagination_path = request.path+'?'
    if category_item is not None:
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

# this is for all products array filter by pagination array
def product_pagination(products,page_num):
    p = Paginator(products,3)
    page_num = page_num
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return [page, p]

# this is for all products within page with pagination
def all_cakes(request):
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

# this is for cake-shop page for view all category products
def shop(request):
    bradcrumb_list = ['cake-shop']
    context = {
        'title':'All Cakes Category',
        'bradcrumb_list':bradcrumb_list,
        'all_category':all_category,
    }
    return render(request, 'products/shop.html',context)

# this class mainly use for single products view user products options controll and validation
# this is add to cart product variation options control
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

    # this is for set user product variation and set subtotal, total, single product price ...
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

# this is mainly set product variation array
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

# this is single product view
def single_product(request, slug):
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
        'options':options,
    }
    return render(request, 'products/single.html',context)
