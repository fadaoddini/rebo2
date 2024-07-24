from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.db.models import Q, Avg, Max, Min, Count, F
import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.cart import Shipping
from order.utils import check_is_active, check_is_ok
from catalogue.utils import check_is_active
from company.models import Company
from info.models import Info
from shop import models, forms
from shop.models import Product, Location
from django.contrib.auth import get_user_model as user_model
from cart.forms import CartAddProductForm


class SingleWeb(View):
    template_name = 'shop/web/single.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        context = dict()
        product = Product.objects.filter(Q(pk=pk) | Q(upc=pk)) \
            .filter(is_active=True).get()

        if request.user.is_anonymous:
            context['product'] = product
        else:
            context['product'] =product
            cart_add_product_form = CartAddProductForm()
            context['cart_add'] = cart_add_product_form

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class CartWeb(View):
    template_name = 'shop/web/cart.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        context = dict()
        my_user = user_model()
        user = my_user.objects.filter(pk=pk).first()

        if request.user.is_anonymous:
            pass
        else:
            context['user'] =user

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


@login_required
@user_passes_test(check_is_active, 'profile')
def location_add(request):
    next = request.POST.get('next', '/')
    # ADD PRODUCT TABLE
    Location.add_location(request)
    return HttpResponseRedirect(next)


@login_required
@user_passes_test(check_is_active, 'profile')
def delete_location(request, code_posti):
    next = request.POST.get('next', '/')
    # ADD PRODUCT TABLE
    Location.delete_location(request, code_posti)
    return HttpResponseRedirect(next)


@require_POST
def location_add_to_cart(request, location_id):
    location = Shipping(request)
    address = get_object_or_404(models.Location, id=location_id)
    form = forms.CartAddLocationForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        location.add(location=address,
                     location_count=form_data['location_count'],
                     update_location=form_data['update']
                     )
    return redirect(reverse('checkout-web'))
