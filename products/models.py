from django.urls import reverse
from django.db import models
import datetime
from django.utils import timezone
# Create your models here.

# this is product category
class Category(models.Model):
    category_name = models.CharField(max_length=120)
    category_slug = models.SlugField(unique=True, max_length=150)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    def __unicode__(self):
        return self.category_name

TIER_SIZE = (
    ('none','None'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('cup cakes','cup cakes'),
)

# cakesize category for different size of cake
class CakeSizeCategory(models.Model):
    size = models.CharField(max_length=120)
    tier = models.CharField(max_length=120, choices=TIER_SIZE, default='none')
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.size

    def __unicode__(self):
        return self.size
# cake flavour category
class FlavourCategory(models.Model):
    category_name = models.CharField(max_length=120)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    def __unicode__(self):
        return self.category_name

# this is cake  flavour variations different flavour price
class Flavour(models.Model):
    flavour_name = models.CharField(max_length=120)
    category = models.ManyToManyField(FlavourCategory)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.flavour_name

# select all category size
# and then make an array options for select input

size_choices_object = CakeSizeCategory.objects.all().values_list('size','size')
size_choice_list = []
for item in size_choices_object:
    size_choice_list.append(item)

# select all category
# and then make an array options for select input

category_list_objects = Category.objects.all().values_list('category_name','category_name')
category_choice_list = []
for item in category_list_objects:
    category_choice_list.append(item)

# select all flavour category
# and then make an array options for select input

flavour_category_list_objects = FlavourCategory.objects.all().values_list('category_name','category_name')
flavour_category_choice_list = []
for item in flavour_category_list_objects:
    flavour_category_choice_list.append(item)

# product review star options
RATING = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
)

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    cake_category = models.CharField(max_length=120, choices=category_choice_list, default='')
    tier = models.CharField(max_length=120, choices=TIER_SIZE, default='none')
    cake_size = models.ManyToManyField(CakeSizeCategory)
    flavour_category = models.CharField(max_length=120, choices=flavour_category_choice_list)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=0)
    slug = models.SlugField(unique=True)
    rating = models.IntegerField(choices=RATING)
    create_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    featured_cake = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('title', 'slug')
    @property
    def get_price_range(self):
        price_range_text = ''
        variation_query = Variation.objects.filter(product=self.id)
        price_range_array = []
        for item_price in variation_query:
            price_range_array.append(item_price.price)
        if(len(price_range_array)>1):
            sorted_price_range_array = sorted(price_range_array)
            price_range_text = '€'+str(sorted_price_range_array[0])+' - €'+str(sorted_price_range_array[len(sorted_price_range_array)-1])
        return "%s %s"%(price_range_text, '')
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse("single_product", kwargs={'slug':self.slug})

# This is for single product multiple image options
class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    featured = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.image

class Variation(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    size = models.CharField(max_length=120, choices=size_choice_list)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.size


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)
    def sizes(self):
        return self.all().filter(size='size')
    
