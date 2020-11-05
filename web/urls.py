from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from . import views
from products import views as product_view
from cart import views as cart_view
from orders import views as order_view
urlpatterns = [
    path('', views.index, name="home"),

    path('product-category/<slug:p_cat>/', product_view.product_category, name="product_category_page"),

    path('about-us', views.about, name="about"),
    path('cake-flavours', views.cake_flavours, name="cake_flavours"),
    path('contacts', views.contacts, name="contacts"),
    path('frequently-asked-questions', views.faqs, name="faqs"),
    # products url
    path('category/', product_view.all_cakes, name="category"),
    path('category/<slug:cat>/', product_view.category, name="category_page"),
    path('cake-shop/', product_view.shop, name="cake_shop"),
    path('all-cakes/', product_view.all_cakes, name="all_cakes"),

    # cart url
    path('cart/', cart_view.view_cart, name="cart"),
    path('add_to_cart/<int:item_id>/', cart_view.add_to_cart, name="add_to_cart"),
    path('remove_item/<int:remove_item_id>/', cart_view.remove_item, name="remove_item"),
    path('update_cart_item/<int:update_item_id>/', cart_view.update_cart_item, name="update_cart_item"),

    # order urls
    path('checkout/', order_view.checkout, name="checkout"),


    path('<slug:slug>/', product_view.single_product, name="single_product"),



]

#/media/{{ product.productimage_set.all.first.image }}
# product.description|truncatechars_html:20
# {% with products|first as first_doc %}{{ first_doc.cake_category }}{% endwith %}
