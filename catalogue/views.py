import datetime
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Avg, Max, Min, Count, F
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model as user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

from bid.models import Bid
from catalogue.models import Product, Category, ProductType, Brand, ProductAttribute, ProductAttributeValue
from catalogue.serializers import ProductSellSerializer, ProductSingleSerializer, TypesSerializer
from catalogue.utils import check_user_active
from company.forms import CompanyForm
from company.models import Company
from config.lib_custom.get_info_by_user import GetInfoByUser
from info.forms import InfoUserForm
from info.models import Info
from order.utils import check_is_active, check_is_ok
from django.http import JsonResponse
import json


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class AddProduct(View):
    template_name = 'web/profile/product/add_product.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        if check_is_ok(request.user, pk):
            context = GetInfoByUser.get_all_info_by_user(request)
            show_item = True
            types = ProductType.objects.all()
            categories = Category.objects.all()
            brands = Brand.objects.all()
            context['types'] = types
            context['categories'] = categories
            context['brands'] = brands
            context['show_item'] = show_item

            return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)
        messages.error(request,
                       "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
        return HttpResponseRedirect(reverse_lazy('index'))


class AddRequest(View):
    template_name = 'web/profile/product/add_request.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        if check_is_ok(request.user, pk):
            context = GetInfoByUser.get_all_info_by_user(request)
            show_item = True
            types = ProductType.objects.all()
            categories = Category.objects.all()
            brands = Brand.objects.all()
            context['types'] = types
            context['categories'] = categories
            context['brands'] = brands
            context['show_item'] = show_item

            return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)
        messages.error(request,
                       "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
        return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active, 'profile')
@user_passes_test(check_user_active, 'profile')
def add_product_web(request, pk):
    if check_is_ok(request.user, pk):
        User = user_model()
        user = User.objects.filter(pk=pk)
        show_item = True
        types = ProductType.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()
        if user.exists():
            user = user.first()
            context = dict()
            context['user'] = user
            context['types'] = types
            context['categories'] = categories
            context['brands'] = brands
            context['show_item'] = show_item
            return render(request, 'web/profile/product/add_product.html', context=context)

    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))




@login_required
@user_passes_test(check_is_active, 'profile')
def add_product(request, pk):
    if check_is_ok(request.user, pk):
        User = user_model()
        user = User.objects.filter(pk=pk)
        show_item = True
        types = ProductType.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()
        if user.exists():
            user = user.first()
            context = dict()
            context['user'] = user
            context['types'] = types
            context['categories'] = categories
            context['brands'] = brands
            context['show_item'] = show_item
            return render(request, 'catalogue/add_product.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active, 'profile')
@user_passes_test(check_user_active, 'profile')
def add_product_web(request, pk):
    if check_is_ok(request.user, pk):
        User = user_model()
        user = User.objects.filter(pk=pk)
        show_item = True
        types = ProductType.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()
        if user.exists():
            user = user.first()
            context = dict()
            context['user'] = user
            context['types'] = types
            context['categories'] = categories
            context['brands'] = brands
            context['show_item'] = show_item
            return render(request, 'catalogue/web/addproduct.html', context=context)

    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@csrf_exempt
def create_chart_top(request):
    if is_ajax(request):
        day = request.POST.get('day')
        pk = request.POST.get('pk')
        amar = {}
        product_type_exist = ProductType.objects.all()
        last_month = datetime.today() - timedelta(days=int(day))
        bazars = Product.objects.filter(sell_buy=1).filter(product_type_id=pk).filter(create_time__gt=last_month)
        price_avg = bazars.aggregate(avg_price=Avg('price'))
        price_max = bazars.aggregate(max_price=Max('price'))
        price_min = bazars.aggregate(min_price=Min('price'))
        bazar_count = bazars.count()
        product_type = ProductType.objects.filter(pk=pk).first()
        if product_type_exist:
            amar['price_avg'] = price_avg['avg_price']
            amar['price_max'] = price_max['max_price']
            amar['price_min'] = price_min['min_price']
            amar['bazar_count'] = bazar_count
            amar['product_type_name'] = product_type.title
            result_amar = list(amar.values())
            result_chart2 = list(bazars.values())
            print("111111111111111111111113")
            print(result_amar)
            print("111111111111111111111113")
            print("222222222222222222222223")
            print(result_chart2)
            print("222222222222222222222223")

            return JsonResponse({
                'msg': result_chart2,
                'result_amar': result_amar
            })
        else:
            return JsonResponse({'msg': 'error'})


@csrf_exempt
def check_type_product_ajax(request):
    if is_ajax(request):
        pk = request.POST.get('pk')
        product_type_exist = ProductType.objects.filter(pk=pk)
        product_attributes = ProductAttribute.objects.filter(product_type=pk)
        if product_attributes:
            form_test = list(product_attributes.values())
            return JsonResponse({'msg': form_test})
        else:
            return JsonResponse({'msg': 'error'})


@csrf_exempt
def check_attr_product_ajax(request):
    if is_ajax(request):
        pk = request.POST.get('pk')
        product_attribute_values = ProductAttributeValue.objects.filter(product_attribute=pk)
        if product_attribute_values:
            form_test = list(product_attribute_values.values())
            return JsonResponse({'msg': form_test})
        else:
            return JsonResponse({'msg': 'error'})


@login_required
@user_passes_test(check_is_active, 'profile')
def form_add_product(request):
    sell_buy = 1
    next = request.POST.get('next', '/')
    # ADD PRODUCT TABLE
    result = Product.add_product(request, sell_buy)
    if result == "100":
        messages.info(request, "محصول شما با موفقیت در سامانه ثبت گردید، "
                               "بعد از تایید توسط کارشناسان قابل نمایش خواهد بود ")
        return HttpResponseRedirect(next)
    elif result == "10":
        messages.error(request, "لطفا عنوانی را برای محصول خود مشخص کنید")
        return HttpResponseRedirect(next)
    elif result == "20":
        messages.error(request, "لطفا قیمت واحد محصول خود را بصورت ریالی درج نمائید")
        return HttpResponseRedirect(next)
    elif result == "30":
        messages.error(request, "لطفا وزن تقریبی موجودی کالای خود را درج نمائید")
        return HttpResponseRedirect(next)
    elif result == "40":
        messages.error(request, "لطفا نوع محصول خود را مشخص نمائید")
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "خطا در ورود اطلاعات محصول، لطفا در ورود اطلاعات دقت لازم را مبذول فرمائید")
        return HttpResponseRedirect(next)


@login_required
@user_passes_test(check_is_active, 'profile')
def form_add_bid_web(request, upc):
    next = request.POST.get('next', '/')
    # ADD PRODUCT TABLE
    result = Bid.add_bid(request, upc)
    if result == "100":
        messages.info(request, "پیشنهاد شما با موفقیت ثبت گردید ")
        return HttpResponseRedirect(next)
    elif result == "400":
        messages.info(request, "پیشنهاد شما با موفقیت بروزرسانی شد")
        return HttpResponseRedirect(next)
    elif result == "20":
        messages.error(request, "لطفا قیمت پیشنهادی خود را بصورت ریالی درج نمائید")
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "خطا ، لطفا در ورود اطلاعات دقت لازم را مبذول فرمائید")
        return HttpResponseRedirect(next)


@login_required
@user_passes_test(check_is_active, 'profile')
def form_bid_ok(request, pk):
    next = request.POST.get('next', '/')
    result = Bid.ok_bid(request, pk)
    if result == "100":
        messages.info(request, "پیشنهاد پذیرفته شد ")
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "خطا ، لطفا مجددا تلاش نمائید")
        return HttpResponseRedirect(next)


@login_required
@user_passes_test(check_is_active, 'profile')
def form_bid_no(request, pk):
    next = request.POST.get('next', '/')
    result = Bid.no_bid(request, pk)
    if result == "100":
        messages.info(request, "پیشنهاد رد شد ")
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "خطا ، لطفا مجددا تلاش نمائید")
        return HttpResponseRedirect(next)


@login_required
@user_passes_test(check_is_active, 'profile')
def form_add_product_web(request):
    sell_buy = 1
    next = request.POST.get('next', '/')
    # ADD PRODUCT TABLE
    result = Product.add_product(request, sell_buy)
    if result == "100":
        messages.info(request, "محصول شما با موفقیت در سامانه ثبت گردید، "
                               "بعد از تایید توسط کارشناسان قابل نمایش خواهد بود ")
        return HttpResponseRedirect(next)
    elif result == "10":
        messages.error(request, "لطفا عنوانی را برای محصول خود مشخص کنید")
        return HttpResponseRedirect(next)
    elif result == "20":
        messages.error(request, "لطفا قیمت واحد محصول خود را بصورت ریالی درج نمائید")
        return HttpResponseRedirect(next)
    elif result == "30":
        messages.error(request, "لطفا وزن تقریبی موجودی کالای خود را درج نمائید")
        return HttpResponseRedirect(next)
    elif result == "40":
        messages.error(request, "لطفا نوع محصول خود را مشخص نمائید")
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "خطا در ورود اطلاعات محصول، لطفا در ورود اطلاعات دقت لازم را مبذول فرمائید")
        return HttpResponseRedirect(next)


@login_required
@user_passes_test(check_is_active, 'profile')
def form_add_request_web(request):
    sell_buy = 2
    next = request.POST.get('next', '/')
    # ADD PRODUCT TABLE
    result = Product.add_product(request, sell_buy)
    if result == "100":
        messages.info(request, "درخواست شما با موفقیت در سامانه ثبت گردید، "
                               "بعد از تایید توسط کارشناسان قابل نمایش خواهد بود ")
        return HttpResponseRedirect(next)
    elif result == "10":
        messages.error(request, "لطفا عنوانی را برای درخواست خود مشخص کنید")
        return HttpResponseRedirect(next)
    elif result == "20":
        messages.error(request, "لطفا قیمت خرید خود را بصورت ریالی درج نمائید")
        return HttpResponseRedirect(next)
    elif result == "30":
        messages.error(request, "لطفا وزن تقریبی نیاز خود را درج نمائید")
        return HttpResponseRedirect(next)
    elif result == "40":
        messages.error(request, "لطفا نوع محصول مورد نظر خود را مشخص نمائید")
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "خطا در ورود اطلاعات درخواست، لطفا در ورود اطلاعات دقت لازم را مبذول فرمائید")
        return HttpResponseRedirect(next)


@login_required
@user_passes_test(check_is_active, 'profile')
def form_add_request(request):
    sell_buy = 2
    next = request.POST.get('next', '/')
    # ADD PRODUCT TABLE
    result = Product.add_product(request, sell_buy)
    if result == "100":
        messages.info(request, "درخواست شما با موفقیت در سامانه ثبت گردید، "
                               "بعد از تایید توسط کارشناسان قابل نمایش خواهد بود ")
        return HttpResponseRedirect(next)
    elif result == "10":
        messages.error(request, "لطفا عنوانی را برای درخواست خود مشخص کنید")
        return HttpResponseRedirect(next)
    elif result == "20":
        messages.error(request, "لطفا قیمت خرید خود را بصورت ریالی درج نمائید")
        return HttpResponseRedirect(next)
    elif result == "30":
        messages.error(request, "لطفا وزن تقریبی نیاز خود را درج نمائید")
        return HttpResponseRedirect(next)
    elif result == "40":
        messages.error(request, "لطفا نوع محصول مورد نظر خود را مشخص نمائید")
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "خطا در ورود اطلاعات درخواست، لطفا در ورود اطلاعات دقت لازم را مبذول فرمائید")
        return HttpResponseRedirect(next)


@login_required
@user_passes_test(check_is_active, 'profile')
def add_request_web(request, pk):
    if check_is_ok(request.user, pk):
        User = user_model()
        user = User.objects.filter(pk=pk)
        show_item = True
        types = ProductType.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()
        if user.exists():
            user = user.first()
            context = dict()
            context['user'] = user
            context['types'] = types
            context['categories'] = categories
            context['brands'] = brands
            context['show_item'] = show_item
            return render(request, 'catalogue/web/addrequest.html', context=context)
        return HttpResponse("متاسفانه اطلاعاتی بابت درخواست شما وجود ندارد")
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active, 'profile')
def add_request(request, pk):
    if check_is_ok(request.user, pk):
        User = user_model()
        user = User.objects.filter(pk=pk)
        show_item = True
        types = ProductType.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()
        if user.exists():
            user = user.first()
            context = dict()
            context['user'] = user
            context['types'] = types
            context['categories'] = categories
            context['brands'] = brands
            context['show_item'] = show_item
            return render(request, 'catalogue/add_request.html', context=context)
        return HttpResponse("متاسفانه اطلاعاتی بابت درخواست شما وجود ندارد")
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active, 'profile')
def my_product_list(request, pk):
    if check_is_ok(request.user, pk):
        User = user_model()
        user = User.objects.filter(pk=pk)
        show_item = True
        if user.exists():
            user = user.first()
            products = user.products.filter(sell_buy=1)
            context = dict()
            context['user'] = user
            context['products'] = products
            context['show_item'] = show_item
            return render(request, 'catalogue/my_product_list.html', context=context)
        return HttpResponse("متاسفانه اطلاعاتی بابت درخواست شما وجود ندارد")
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active, 'profile')
def my_request_list(request, pk):
    if check_is_ok(request.user, pk):
        User = user_model()
        user = User.objects.filter(pk=pk)
        show_item = True
        if user.exists():
            user = user.first()
            products = user.products.filter(sell_buy=2)
            context = dict()
            context['user'] = user
            context['products'] = products
            context['show_item'] = show_item
            return render(request, 'catalogue/my_request_list.html', context=context)
        return HttpResponse("متاسفانه اطلاعاتی بابت درخواست شما وجود ندارد")
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active, 'profile')
def bazar_sell(request, pk):
    bazars = Product.objects.filter(sell_buy=1).filter(product_type_id=pk)
    price_avg = bazars.aggregate(avg_price=Avg('price'))
    price_max = bazars.aggregate(max_price=Max('price'))
    price_min = bazars.aggregate(min_price=Min('price'))
    bazar_count = bazars.count()
    product_type = ProductType.objects.filter(pk=pk).first()
    show_item = True
    if bazars:
        context = dict()
        context['bazars'] = bazars
        context['show_item'] = show_item
        context['product_type'] = product_type
        context['price_avg'] = price_avg['avg_price']
        context['price_max'] = price_max['max_price']
        context['price_min'] = price_min['min_price']
        context['bazar_count'] = bazar_count
        return render(request, 'catalogue/bazar_sell.html', context=context)
    return HttpResponse("متاسفانه اطلاعاتی بابت درخواست شما وجود ندارد")


@login_required
@user_passes_test(check_is_active, 'profile')
def bazar_sell_web(request, pk):
    bazars = Product.objects.filter(sell_buy=1).filter(product_type_id=pk)
    price_avg = bazars.aggregate(avg_price=Avg('price'))
    price_max = bazars.aggregate(max_price=Max('price'))
    price_min = bazars.aggregate(min_price=Min('price'))
    bazar_count = bazars.count()
    product_type = ProductType.objects.filter(pk=pk).first()
    show_item = True
    if bazars:
        context = dict()
        context['bazars'] = bazars
        context['show_item'] = show_item
        context['product_type'] = product_type
        context['price_avg'] = price_avg['avg_price']
        context['price_max'] = price_max['max_price']
        context['price_min'] = price_min['min_price']
        context['bazar_count'] = bazar_count
        return render(request, 'catalogue/web/statistics.html', context=context)
    return HttpResponse("متاسفانه اطلاعاتی بابت درخواست شما وجود ندارد")


@login_required
@user_passes_test(check_is_active, 'profile')
def bazar_buy(request):
    bazars = Product.objects.filter(sell_buy=2)
    show_item = True
    if bazars:
        context = dict()
        context['bazars'] = bazars
        context['show_item'] = show_item
        return render(request, 'catalogue/bazar_buy.html', context=context)
    return HttpResponse("متاسفانه اطلاعاتی بابت درخواست شما وجود ندارد")


def product_list(request):
    products_filter = Product.objects.filter(is_active=True)
    products_exclude = Product.objects.exclude(is_active=False)
    category_first = Category.objects.first()
    category_last = Category.objects.last()
    category = Category.objects.all()
    brand = Brand.objects.first()

    products = Product.objects.filter(is_active=True, category_id=4)

    products = Product.objects.prefetch_related('category').all()
    products = Product.objects.select_related('category', 'brand').all()
    product_type = ProductType.objects.first()
    # product_create = Product.objects.create(
    #     product_type=product_type,
    #     upc=8456113,
    #     title="خرمای مضافتی تست",
    #     description="",
    #     category=category,
    #     brand=brand
    # )

    # context = "".join([f"{product.title} ===>>>> {product.upc}"
    #                   f"  |||| - {product.category.name} - |||| "
    #                   f"  |||| - {product.brand.name} - |||| \n"
    #                   for product in products])
    # return HttpResponse(context)
    context = dict()
    products = Product.objects.all()
    context['products'] = products
    context['category'] = category
    print(products)
    return render(request, 'catalogue/product_list.html', context=context)


class ProductDetail(View):
    template_name = 'catalogue/web/single.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        context = dict()
        product = Product.objects.filter(Q(pk=pk) | Q(upc=pk)) \
            .filter(is_active=True).filter(
            expire_time__gt=datetime.now()).get()
        if product:
            print("yessssss")
        else:
            print("noooooo")
        product_type = product.product_type
        learns = product_type.learns.all()
        context['learns'] = learns
        bids = Bid.objects.filter(product=product).all()
        if request.user.is_anonymous:

            context['product'] = product
            context['bids'] =bids
            topprice = bids.aggregate(maxprice=Max(F('price')))
            context['topprice'] = topprice['maxprice']
        else:
            context['product'] =product
            context['bids'] = bids
            user_bid = request.user.bids.first()
            if user_bid:
                result_show = user_bid.result
                context['result_show'] = result_show
                top_price_bid = Bid.objects.filter(product=product).order_by('-price').first()
                context['top_bid_price'] = top_price_bid
            else:
                context['result_show'] = False
                context['top_bid_price'] = None
            topprice = bids.aggregate(maxprice=Max(F('price')))
            context['topprice'] = topprice['maxprice']
            context['info'] = Info.objects.filter(user=request.user).first()
            context['company'] = Company.objects.filter(user=request.user).first()
            form_info = InfoUserForm()
            context['form_info'] = form_info
            form_company = CompanyForm()
            context['form_company'] = form_company

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class RequestDetail(View):
    template_name = 'catalogue/web/single.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        context = dict()
        print("product")

        try:
            product = Product.objects.filter(Q(pk=pk) | Q(upc=pk)) \
                .filter(is_active=True).filter(expire_time__gt=datetime.now()).get()
        except ObjectDoesNotExist:
            messages.error(request, "هنوز تائید نشده است!")
            return HttpResponseRedirect(reverse_lazy('index'))
        product_type = product.product_type
        learns = product_type.learns.all()
        context['learns'] = learns
        bids = Bid.objects.filter(product=product).all()
        if request.user.is_anonymous:

            context['product'] = product
            context['bids'] =bids
            topprice = bids.aggregate(maxprice=Max(F('price')))
            context['topprice'] = topprice['maxprice']
        else:
            context['product'] =product
            context['bids'] = bids
            topprice = bids.aggregate(maxprice=Max(F('price')))
            context['topprice'] = topprice['maxprice']
            context['info'] = Info.objects.filter(user=request.user).first()
            context['company'] = Company.objects.filter(user=request.user).first()
            form_info = InfoUserForm()
            context['form_info'] = form_info
            form_company = CompanyForm()
            context['form_company'] = form_company

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


def category_products(request, pk):
    try:
        queryset = Category.objects.prefetch_related('products')
        if queryset:
            category = queryset.get(pk=pk)
            products = Product.objects.filter(category=category)
        else:
            return HttpResponse("متاسفانه چیزی پیدا نشد!")
    except Category.DoesNotExist:
        return HttpResponse("متاسفانه دسته بندی با این مشخصات ثبت نشده است")
    if products:
        context = "".join([f"{product.title} ===>>>> {product.upc}"
                           f"  |||| - {product.category.name} - |||| \n"
                           for product in products])
        return HttpResponse(context)
    else:
        return HttpResponse("متاسفانه چیزی پیدا نشد!")


def brand_products(request, pk):
    try:
        queryset = Brand.objects.prefetch_related('products')
        if queryset:
            brand = queryset.get(pk=pk)
            products = Product.objects.filter(brand=brand)
        else:
            return HttpResponse("متاسفانه چیزی پیدا نشد!")
    except Brand.DoesNotExist:
        return HttpResponse("متاسفانه برندی با این مشخصات ثبت نشده است")
    if products:
        context = "".join([f"{product.title} ===>>>> {product.upc}"
                           f"  |||| - {product.brand.name} - |||| \n"
                           for product in products])
        return HttpResponse(context)
    else:
        return HttpResponse("متاسفانه چیزی پیدا نشد!")


class TypesApi(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        context = dict()
        types = ProductType.objects.all()
        serializer = TypesSerializer(types, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class ProductApi(APIView):

    # permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sortby = body['sortby']
        type = body['type']
        if type == "sell":
            if sortby == "newest":
                product = Product.objects.filter(sell_buy=1).order_by('-modified_time')
            elif sortby == "highestWeight":
                product = Product.objects.filter(sell_buy=1).order_by('-weight')
            elif sortby == "lowestWeight":
                product = Product.objects.filter(sell_buy=1).order_by('weight')
        elif type == "buy":
            if sortby == "newest":
                product = Product.objects.filter(sell_buy=2).order_by('-modified_time')
            elif sortby == "highestWeight":
                product = Product.objects.filter(sell_buy=2).order_by('-weight')
            elif sortby == "lowestWeight":
                product = Product.objects.filter(sell_buy=2).order_by('weight')
        else:
            if sortby == "newest":
                product = Product.objects.all().order_by('-modified_time')
            elif sortby == "highestWeight":
                product = Product.objects.all().order_by('-weight')
            elif sortby == "lowestWeight":
                product = Product.objects.all().order_by('weight')

        serializer = ProductSellSerializer(product, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class TestApi(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        products = Product.objects.all().data
        return Response(products, content_type='application/json; charset=UTF-8')


class ProductSingleApi(APIView):

    # permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        pk = body['id']
        product = Product.objects.filter(pk=pk).first()

        serializer = ProductSingleSerializer(product)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class ProductWeb(View):
    template_name = 'catalogue/web/index.html'

    def get(self, request, *args, **kwargs):
        learns = Product.objects.filter(user=request.user).all()
        return render(request, template_name=self.template_name, context={'learns': learns},
                      content_type=None, status=None, using=None)


class BazarWeb(View):
    template_name = 'catalogue/web/bazar.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        products = Product.objects.all()
        context['products'] = products
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class InBazarWeb(View):
    template_name = 'catalogue/web/inbazar.html'

    def get(self, request, pk, *args, **kwargs):
        context = dict()
        title = ProductType.objects.filter(pk=pk).first()
        # seller
        sellers = Product.objects.filter(sell_buy=1).filter(product_type_id=pk)\
            .filter(expire_time__gt=datetime.now())
        context['sellers'] = sellers.order_by('price')[:30]

        # buyer
        buyers = Product.objects.filter(sell_buy=2).filter(product_type_id=pk)\
            .filter(expire_time__gt=datetime.now())
        context['buyers'] = buyers.order_by('-price')[:30]

        context['title'] = title
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class AllProductWeb(View):
    template_name = 'catalogue/web/list.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        products = Product.objects.filter(user=request.user).filter(sell_buy=1).all()
        context['count'] = products.count()
        context['products'] = products
        context['titr'] = "محصولات"
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class AllRequestWeb(View):
    template_name = 'catalogue/web/list.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        products = Product.objects.filter(user=request.user).filter(sell_buy=2).all()
        context['products'] = products
        context['titr'] = "درخواست های"
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class AllProductAndRequestWeb(View):
    template_name = 'catalogue/web/list.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        products = Product.objects.filter(user=request.user).all()
        context['products'] = products
        context['titr'] = "محصولات"
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)

