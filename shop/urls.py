from django.urls import path

from shop.views import SingleWeb, CartWeb, location_add, location_add_to_cart, delete_location

urlpatterns = [
    path('single/<int:pk>/', SingleWeb.as_view(), name='shop-single-web'),
    path('cart/<int:pk>/', CartWeb.as_view(), name='shop-cart-web'),
    path('add_location/', location_add, name='location-add-web'),
    path('delete_location/<int:code_posti>/', delete_location, name='delete_location'),
    path('add_location/<int:location_id>/', location_add_to_cart, name='location-add-web-to-cart'),
]