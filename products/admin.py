from django.contrib import admin
#from .models import Product, CakeCategory, ProductImage, Flavour, Variation, CakeSizeCategory
from .models import Product, ProductImage, Category, Flavour, CakeSizeCategory
# Register your models here.


@admin.register(Category)
class ProductCakeSizeCategory(admin.ModelAdmin):
    list_display = ['category_name','category_slug', 'updated', 'active']


@admin.register(Flavour)
class FlavourAdmin(admin.ModelAdmin):
    list_display = ['flavour_name','price', 'active']
    search_fields = ['flavour_name']
    list_editable = ["price"]

@admin.register(CakeSizeCategory)
class ProductCakeSizeCategory(admin.ModelAdmin):
    list_display = ['size','tier', 'active']

class ProductImageAdmin(admin.StackedInline):
    model=ProductImage



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','cake_category', 'price', 'rating', 'tier', 'updated']
    list_display_links = ["title"]
    list_filter = ['create_date','title']
    search_fields = ['title', 'description']
    list_editable = ['price', "rating"]
    inlines = [ProductImageAdmin]
    class Meta:
        model = Product

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

# class ProductCakeSizeCategory(admin.StackedInline):
#     model=CakeSizeCategory
#
# class ProductPriceVariation(admin.StackedInline):
#     model=Variation
#
# # class ProductFlavourVariation(admin.StackedInline):
# #     model=Flavour
#

#
# #admin.site.register(Post, PostModelAdmin)
# #admin.site.register(Post, ProductImage)

#
#
# @admin.register(Variation)
# class ProductPriceVariation(admin.ModelAdmin):
#     list_display = ['size','price', 'active']
#

#

#
# @admin.register(CakeCategory)
# class CakeCategoryAdmin(admin.ModelAdmin):
#     list_display = ['category_name','category', 'active']

# @admin.register(ProductCategory)
# class ProductCategoryAdmin(admin.ModelAdmin):
#     list_display = ['category_name','category', 'active']
