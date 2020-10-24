from django.contrib import admin
from .models import Product, CakeCategory, ProductImage, Flavour, Variation, CakeSizeCategory
# Register your models here.

class ProductImageAdmin(admin.StackedInline):
    model=ProductImage
class ProductCakeSizeCategory(admin.StackedInline):
    model=CakeSizeCategory

class ProductPriceVariation(admin.StackedInline):
    model=Variation

# class ProductFlavourVariation(admin.StackedInline):
#     model=Flavour

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','create_date', 'updated']
    list_display_links = ["title"]
    list_filter = ['create_date','title']
    search_fields = ['title', 'description']
    #list_editable = ["title"]
    inlines = [ProductPriceVariation, ProductImageAdmin,]
    class Meta:
        model = Product

#admin.site.register(Post, PostModelAdmin)
#admin.site.register(Post, ProductImage)
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Variation)
class ProductPriceVariation(admin.ModelAdmin):
    pass

@admin.register(CakeSizeCategory)
class ProductCakeSizeCategory(admin.ModelAdmin):
    list_display = ['size','tier', 'active']

@admin.register(Flavour)
class ProductFlavourVariation(admin.ModelAdmin):
    list_display = ['flavour_name','price', 'active']
    search_fields = ['flavour_name']
    list_editable = ["price"]

@admin.register(CakeCategory)
class CakeCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','category', 'active']
