from django.contrib import admin
from django.urls import path
from . import views
from products import views as product_view
urlpatterns = [
    path('', views.index, name="home"),

    path('product-category/<slug:p_cat>/', product_view.product_category, name="product_category_page"),

    path('about-us', views.about, name="about"),
    path('cake-flavours', views.cake_flavours, name="cake_flavours"),
    path('contacts', views.contacts, name="contacts"),
    path('frequently-asked-questions', views.faqs, name="faqs"),

    path('category/', product_view.all_cakes, name="category"),
    path('category/<slug:cat>/', product_view.category, name="category_page"),
    path('cake-shop/', product_view.shop, name="cake_shop"),
    path('all-cakes/', product_view.all_cakes, name="all_cakes"),
    path('updated_item/', product_view.updated_item, name="updated_item"),
    path('<slug:slug>/', product_view.single_product, name="single_product"),



]

#/media/{{ product.productimage_set.all.first.image }}
# product.description|truncatechars_html:20
# {% with products|first as first_doc %}{{ first_doc.cake_category }}{% endwith %}
