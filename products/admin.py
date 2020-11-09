from django.contrib import admin
#from .models import Product, CakeCategory, ProductImage, Flavour, Variation, CakeSizeCategory
from .models import Product, ProductImage, Variation, Category, Flavour, CakeSizeCategory
# Register your models here.

# register for cake category
@admin.register(Category)
class ProductCakeSizeCategory(admin.ModelAdmin):
    list_display = ['category_name','category_slug', 'updated', 'active']

# register for cake flavour
@admin.register(Flavour)
class FlavourAdmin(admin.ModelAdmin):
    list_display = ['flavour_name', 'category', 'price', 'active']
    search_fields = ['flavour_name']
    list_editable = ['category', "price"]

# register for cake size category
@admin.register(CakeSizeCategory)
class ProductCakeSizeCategory(admin.ModelAdmin):
    list_display = ['size','tier', 'active']

# this class for product images inside product proudct panel
class ProductImageAdmin(admin.StackedInline):
    model=ProductImage

# this class for product price variation inside product proudct panel
class ProductPriceVariation(admin.StackedInline):
    model=Variation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','cake_category', 'price', 'rating', 'tier', 'updated']
    list_display_links = ["title"]
    list_filter = ['create_date','title']
    search_fields = ['title', 'description']
    list_editable = ['price', "rating"]
    inlines = [ProductImageAdmin, ProductPriceVariation]
    class Meta:
        model = Product

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass



@admin.register(Variation)
class ProductPriceVariation(admin.ModelAdmin):
    list_display = ['size','price', 'active']



# class ProductCakeSizeCategory(admin.StackedInline):
#     model=CakeSizeCategory
#

#
# # class ProductFlavourVariation(admin.StackedInline):
# #     model=Flavour
#

#
# #admin.site.register(Post, PostModelAdmin)
# #admin.site.register(Post, ProductImage)

#
#

#

#

#
# @admin.register(CakeCategory)
# class CakeCategoryAdmin(admin.ModelAdmin):
#     list_display = ['category_name','category', 'active']

# @admin.register(ProductCategory)
# class ProductCategoryAdmin(admin.ModelAdmin):
#     list_display = ['category_name','category', 'active']
