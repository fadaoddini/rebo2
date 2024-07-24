from django.urls import path

from cart.views import cart_add, remove_product, CartWeb, CheckoutWeb

urlpatterns = [
    path('', CartWeb.as_view(), name='cart-details-web'),
    path('checkout/', CheckoutWeb.as_view(), name='checkout-web'),
    path('add/<int:product_id>/', cart_add, name='cart-add-web'),
    path('remove/<int:product_id>/', remove_product, name='cart-remove-product-web'),

]