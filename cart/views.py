from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q, Avg, Max, Min, Count, F
from django.contrib.auth import get_user_model as user_model
from cart import forms
from shop import forms as form_shop
from cart.cart import Cart, Shipping
from shop import models
from shop.models import Location


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(models.Product, id=product_id)
    form = forms.CartAddProductForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        cart.add(product=product,
                 product_count=form_data['product_count'],
                 update_count=form_data['update'])
    return redirect(reverse('cart-details-web'))


class CartWeb(View):
    template_name = 'shop/web/cart.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()

        if request.user.is_anonymous:
            pass
        else:
            cart = Cart(request)
            context['cart'] = cart
            for item in cart:
                item['update_product_count_form'] = forms.CartAddProductForm(
                    initial={
                        'product_count': item['product_count'],
                        'update': True
                    }
                )

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class CheckoutWeb(View):
    template_name = 'shop/web/checkout.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        user = request.user
        if request.user.is_anonymous:
            pass
        else:
            cart = Cart(request)
            location_cart = Shipping(request)
            context['cart'] = cart
            context['location_cart'] = location_cart
            context['form_location'] = form_shop.LocationForm()
            locations = Location.objects.filter(user=user).all()
            context['locations'] = locations
            context['update_location_form'] = forms.CartAddLocationForm(
                initial={
                    'location_count': 1,
                    'update': True
                }
            )

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


def remove_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(models.Product, id=product_id)
    cart.remove_product_in_cart(product)
    return redirect(reverse('cart-details-web'))