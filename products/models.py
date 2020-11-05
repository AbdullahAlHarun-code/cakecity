#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models

# Create your models here.

# Cake Category

CAKES_CATEGORY = (('0', 'Uncategorized'), ('novelty-cakes',
                  'Novelty Cakes'), ('wedding-cakes', 'Wedding Cakes'),
                  ('corporate-cakes', 'Corporate Cakes'))


class CakeCategory(models.Model):

    category_name = models.CharField(max_length=120)
    category_slug = models.SlugField(unique=True, max_length=150)
    category = models.CharField(max_length=120, choices=CAKES_CATEGORY,
                                default='0')
    image = models.ImageField(upload_to='category/', null=True,
                              blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    def get_category_name_by_slug(self):
        category_title = ''
        for (x, y) in CAKES_CATEGORY:
            if x == self.category:
                category_title = y
        return category_title

    def __unicode__(self):
        return self.category_name


TIER_SIZE = (
    ('none', 'None'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('cup cakes', 'cup cakes'),
    )


class CakeSizeCategory(models.Model):

    size = models.CharField(max_length=120)
    tier = models.CharField(max_length=120, choices=TIER_SIZE,
                            default='none')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.size

    def __unicode__(self):
        return self.size


size_choices_object = CakeSizeCategory.objects.all().values_list('size'
        , 'size')
size_choice_list = []
for item in size_choices_object:
    size_choice_list.append(item)

category_list_objects = \
    CakeCategory.objects.all().values_list('category_name',
        'category_name')
category_choice_list = []
for item in category_list_objects:
    category_choice_list.append(item)

RATING = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class Product(models.Model):

    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    cake_category = models.CharField(max_length=120,
            choices=category_choice_list)
    tier = models.CharField(max_length=120, choices=TIER_SIZE,
                            default='none')
    cake_size = models.ManyToManyField(CakeSizeCategory)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    slug = models.SlugField(unique=True)
    rating = models.IntegerField(max_length=120, choices=RATING)
    create_date = models.DateTimeField(auto_now_add=True,
            auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    featured_cake = models.BooleanField(default=True)
    active = models.BooleanField(default=False)

    class Meta:

        unique_together = ('title', 'slug')

    @property
    def get_price_range(self):
        variation_query = Variation.objects.filter(product=self.id)
        price_range_array = []
        for item_price in variation_query:
            price_range_array.append(item_price.price)
        if len(price_range_array) > 1:
            sorted_price_range_array = sorted(price_range_array)
            price_range_text = '\xe2\x82\xac' \
                + str(sorted_price_range_array[0]) + ' - \xe2\x82\xac' \
                + str(sorted_price_range_array[len(sorted_price_range_array)
                      - 1])
        return '%s %s' % (price_range_text, '')

    def __unicode__(self):
        return self.title

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse('single_product', kwargs={'slug': self.slug})


class ProductImage(models.Model):

    product = models.ForeignKey(Product, default=None,
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    featured = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.image


class VariationManager(models.Manager):

    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(size='size')


class Variation(models.Model):

    product = models.ForeignKey(Product, default=None,
                                on_delete=models.CASCADE)
    size = models.CharField(max_length=120, choices=size_choice_list,
                            default=None)
    price = models.DecimalField(max_digits=100, decimal_places=2,
                                default=0, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.size


FLAVOUR_CATEGORY = (
    ('tier cakes', 'tier cakes'),
    ('cupcakes', 'cupcakes'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('cup cakes', 'cup cakes'),
    )


class Flavour(models.Model):

    flavour_name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=50, decimal_places=2,
                                default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.flavour_name
