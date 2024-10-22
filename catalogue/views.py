import datetime
import json
import random
from datetime import datetime, timedelta
import math
from django.conf import settings
from django.db import transaction
from django.db.models import Prefetch
from bid.serializers import BidSerializer
from login.views import CookieJWTAuthentication
from order.models import Payment, Gateway
from order.utils import zpal_request_handler
from persiantools.jdatetime import JalaliDate
from django.contrib import messages
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Avg, Max, Min, F, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from collections import defaultdict
from bid.models import Bid
from catalogue.models import Product, Category, ProductType, Brand, ProductAttribute, ProductAttributeValue, \
    ProductImage, ProductAttr
from catalogue.serializers import ProductSellSerializer, ProductSingleSerializer, TypesSerializer, \
    ProductTypeSerializer, ProductAttributeSerializer, ProductAttributeValueSerializer, ApiProductSerializer, \
    SingleProductSerializer, SellSingleProductSerializer, BuySingleProductSerializer, CategoryTypeSerializer, \
    ApiAllProductSerializer
from catalogue.utils import check_user_active
from company.forms import CompanyForm
from company.models import Company
from config.lib_custom.get_info_by_user import GetInfoByUser
from info.forms import InfoUserForm
from info.models import Info
from order.utils import check_is_active, check_is_ok
from .serializers import CategorySerializer


class ProductTypeListAPIView(generics.ListAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    # ویو برای لیست کردن نوع محصولات


class ProductAttributeListAPIView(generics.ListAPIView):
    serializer_class = ProductAttributeSerializer

    def get_queryset(self):
        product_type_id = self.request.query_params.get('product_type_id')
        if product_type_id:
            return ProductAttribute.objects.filter(product_type_id=product_type_id)
        return ProductAttribute.objects.none()
    # ویو برای لیست کردن ویژگی‌های محصولات بر اساس نوع محصول


class AttributeValueListAPIView(generics.ListAPIView):
    serializer_class = ProductAttributeValueSerializer

    def get_queryset(self):
        attribute_id = self.request.query_params.get('attribute_id')
        if attribute_id:
            return ProductAttributeValue.objects.filter(product_attribute_id=attribute_id)
        return ProductAttributeValue.objects.none()
    # ویو برای لیست کردن مقادیر ویژگی‌های محصولات بر اساس شناسه ویژگی


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # ویو برای لیست کردن دسته‌بندی‌ها


class ApiProductCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



    def post(self, request, *args, **kwargs):
        user = request.user

        # دریافت داده‌های فرم
        price = request.data.get('price')
        weight = request.data.get('weight')
        sell_buy_code = request.data.get('sell_buy')  # دریافت مقدار sell_buy
        warranty = request.data.get('warranty') == 'True'
        expire_time_days = request.data.get('expire_time')
        description = request.data.get('description')
        product_type_id = request.data.get('product_type')
        attrs = request.data.get('attrs')
        attrs = json.loads(attrs) if attrs else []

        # بررسی تاریخ انقضا
        if expire_time_days:
            expire_time = timezone.now() + timezone.timedelta(days=int(expire_time_days))
        else:
            expire_time = None



        # تبدیل مقدار sell_buy از عدد به متن
        if sell_buy_code == '1':
            sell_buy = Product.SELL
        else:
            sell_buy = Product.BUY

        # بررسی نوع محصول
        product_type = get_object_or_404(ProductType, id=product_type_id)

        # ذخیره محصول
        upc = random.randint(11111111111111111, 99999999999999999)
        product = Product(
            user=user,
            sell_buy=sell_buy,
            product_type=product_type,
            upc=upc,
            price=price,
            weight=weight,
            description=description,
            is_successful=False,
            warranty=warranty,
            is_active=False,  # محصول به صورت پیش‌فرض غیرفعال است
            expire_time=expire_time
        )
        product.save()

        # ذخیره تصاویر
        num_images = int(request.data.get('numpic', 0))

        for i in range(num_images):
            image = request.FILES.get(f'image{i}')
            if image:
                product_image = ProductImage(image=image, product=product)
                product_image.save()

        # ذخیره ویژگی‌های محصول
        for attr in attrs:
            attribute = get_object_or_404(ProductAttribute, id=attr['attr'])
            attribute_value = get_object_or_404(ProductAttributeValue, id=attr['value'])
            ProductAttr(type=product_type, attr=attribute, value=attribute_value, product=product).save()

        return Response({"status": "success", "message": "Product added successfully!"}, status=status.HTTP_201_CREATED)


class ApiProductDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')  # دریافت ID محصول از داده‌های درخواست

        if not product_id:
            return Response({"status": "error", "message": "Product ID is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # دریافت محصول با استفاده از ID
        product = get_object_or_404(Product, id=product_id)

        # بررسی مالکیت محصول (اختیاری، فقط اگر بخواهید که فقط مالک بتواند محصول را حذف کند)
        if product.user != request.user:
            return Response({"status": "error", "message": "You do not have permission to delete this product"},
                            status=status.HTTP_403_FORBIDDEN)

        # حذف محصول
        product.delete()

        return Response({"status": "success", "message": "Product deleted successfully!"},
                        status=status.HTTP_204_NO_CONTENT)


class PaymentApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=400)

        user = request.user
        upc = body.get('product_id')
        upc = int(upc)
        product = Product.objects.filter(upc=upc, user=user).first()

        if not product:
            return Response({
                "status": "error",
                "message": "محصول یافت نشد."
            }, status=status.HTTP_404_NOT_FOUND)

        amount = 25000  # فرض می‌کنیم که مقدار پرداخت همان قیمت محصول است
        mobile = user.mobile  # فرض می‌کنیم که شماره موبایل کاربر در مدل User ذخیره شده است

        payment_link, authority = zpal_request_handler(
            settings.ZARRINPAL['merchant_id'],
            amount,
            "ثبت یا درخواست محصول عمده",
            None,
            mobile,
            f"{settings.ADDRESS_SERVER}/payment/verify/"  # استفاده از ADDRESS_SERVER
        )

        if payment_link:
            # ایجاد یک رکورد پرداخت در دیتابیس
            Payment.create_payment(authority, amount, user, product)  # اضافه کردن product به متد create_payment

            return Response({
                "status": "success",
                "payment_link": payment_link
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "خطا در ایجاد لینک پرداخت."
        }, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        authority = request.query_params.get('authority')
        payment_status = request.query_params.get('status')  # وضعیت پرداخت از زارین‌پال


        payment = Payment.objects.filter(authority=authority).first()
        if payment:
            # استفاده از درگاه ثابت zarrinpal
            gateway = Gateway.objects.filter(gateway_code="zarrinpal").first()
            if gateway is None:
                return Response({
                    "status": "error",
                    "message": "درگاه پرداخت فعال یافت نشد."
                }, status=status.HTTP_400_BAD_REQUEST)

            # متد verify را با استفاده از شیء gateway به‌روز رسانی کنید
            verified = payment.verify({
                'authority': authority,
                'status': payment_status
            })

            if verified and payment_status == "OK":
                with transaction.atomic():
                    # پرداخت موفقیت‌آمیز بوده است، محصول را به‌روزرسانی کنید
                    if payment.product:
                        product = Product.objects.filter(upc=payment.product.upc).first()
                        if product:
                            product.is_successful = True
                            product.save()
                    payment.is_paid = True
                    payment.save()

                # کاربر را به صفحه مورد نظر هدایت کنید
                return Response({
                    "status": "success",
                    "message": "پرداخت با موفقیت انجام شد."
                }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "پرداخت ناموفق بود."
        }, status=status.HTTP_400_BAD_REQUEST)


class ProductByIdAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        product = Product.objects.filter(pk=product_id).first()
        if product:
            # اگر محصول پیدا شد، به عنوان JSON برگردانده می‌شود
            serializer = ProductSellSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # اگر محصول پیدا نشد، وضعیت خطا برگردانده می‌شود
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class ProductNotPayMeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product = Product.objects.filter(user=user).filter(is_successful=False).all()
        if product:
            # اگر محصول پیدا شد، به عنوان JSON برگردانده می‌شود
            serializer = ProductSellSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # اگر محصول پیدا نشد، وضعیت خطا برگردانده می‌شود
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class ProductNotActiveMeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product = Product.objects.filter(user=user).filter(is_successful=True).filter(is_active=False).all()
        if product:
            # اگر محصول پیدا شد، به عنوان JSON برگردانده می‌شود
            serializer = ProductSellSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # اگر محصول پیدا نشد، وضعیت خطا برگردانده می‌شود
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class ProductActiveMeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product = Product.objects.filter(user=user).filter(is_successful=True).filter(is_active=True).all()
        if product:
            # اگر محصول پیدا شد، به عنوان JSON برگردانده می‌شود
            serializer = ProductSellSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # اگر محصول پیدا نشد، وضعیت خطا برگردانده می‌شود
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


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


class BazarStatsApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        days = request.GET.get('days', '7')  # پیش‌فرض به 7 روز
        last_month = datetime.today() - timedelta(days=int(days))

        # فیلتر محصولات با نوع و نوع فروش
        bazars = Product.objects.filter(sell_buy=1, product_type_id=pk, create_time__gt=last_month, is_active=True)
        product_type = ProductType.objects.filter(pk=pk).first()

        if not bazars.exists() or not product_type:
            return Response({"detail": "اطلاعاتی برای درخواست شما موجود نیست."}, status=status.HTTP_404_NOT_FOUND)

        # ایجاد دیکشنری برای ذخیره داده‌های روزانه
        daily_data = defaultdict(lambda: {'min_price': float('inf'), 'max_price': float('-inf')})

        # پردازش داده‌ها
        for product in bazars:
            date = product.create_time.date()
            daily_data[date]['min_price'] = min(daily_data[date]['min_price'], product.price)
            daily_data[date]['max_price'] = max(daily_data[date]['max_price'], product.price)

        # آماده‌سازی داده‌های نهایی
        dates = []
        min_prices = []
        max_prices = []
        current_date = datetime.today()

        for i in range(int(days)):
            date = (current_date - timedelta(days=i)).date()
            shamsi_date = JalaliDate(date).strftime('%Y/%m/%d')  # تبدیل تاریخ به شمسی
            min_price = daily_data[date]['min_price'] if daily_data[date]['min_price'] != float('inf') else None
            max_price = daily_data[date]['max_price'] if daily_data[date]['max_price'] != float('-inf') else None

            if min_price is not None:
                dates.append(shamsi_date)
                min_prices.append(min_price)
                max_prices.append(max_price)

        # مرتب‌سازی بر اساس تاریخ‌های شمسی
        sorted_dates = sorted(set(dates))
        sorted_min_prices = [min_prices[dates.index(date)] for date in sorted_dates]
        sorted_max_prices = [max_prices[dates.index(date)] for date in sorted_dates]

        # محاسبه آمار کلی
        price_avg = bazars.aggregate(avg_price=Avg('price'))['avg_price']
        price_max = bazars.aggregate(max_price=Max('price'))['max_price']
        price_min = bazars.aggregate(min_price=Min('price'))['min_price']
        bazar_count = bazars.count()

        # رند کردن قیمت میانگین
        if price_avg is not None:
            price_avg = math.floor(price_avg / 1000) * 1000  # رند کردن به نزدیک‌ترین هزارگان

        # آماده‌سازی داده‌ها
        stats_data = {
            'dates': sorted_dates,
            'min_prices': sorted_min_prices,
            'max_prices': sorted_max_prices,
            'price_avg': price_avg if price_avg is not None else 0,
            'price_max': price_max if price_max is not None else 0,
            'price_min': price_min if price_min is not None else 0,
            'bazar_count': bazar_count,
            'product_type': ProductTypeSerializer(product_type).data
        }

        return Response(stats_data, status=status.HTTP_200_OK)


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


class AllTypeApi(APIView):
    # اضافه کردن احراز هویت
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        print("iiiiii")
        print("Headers: ", request.headers)
        print("Authorization: ", request.headers.get('Authorization'))

        print("request************************************")
        print(request)


        # فراخوانی تمام داده‌ها
        types = ProductType.objects.all()

        # گروه‌بندی بر اساس دسته‌بندی
        grouped_data = self.group_by_category(types)

        # سریالایزر برای داده‌های گروه‌بندی شده
        serializer = CategoryTypeSerializer(grouped_data, many=True)

        # بازگشت پاسخ با ساختار جدید
        return Response(serializer.data, content_type='application/json; charset=UTF-8')

    def group_by_category(self, product_types):
        # تابعی برای گروه‌بندی محصولات بر اساس دسته‌بندی
        grouped_data = defaultdict(lambda: {'category': '', 'cat_id': 0, 'types': []})

        for product in product_types:
            category_name = product.category.name
            category_id = product.category.id
            grouped_data[category_name]['category'] = category_name
            grouped_data[category_name]['cat_id'] = category_id
            grouped_data[category_name]['types'].append(product)

        return list(grouped_data.values())




class AllTypeWebApi(APIView):
    # اضافه کردن احراز هویت
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        print("iiiiii")
        print("Headers: ", request.headers)
        print("Authorization: ", request.headers.get('Authorization'))

        print("request************************************")
        print(request)


        # فراخوانی تمام داده‌ها
        types = ProductType.objects.all()

        # گروه‌بندی بر اساس دسته‌بندی
        grouped_data = self.group_by_category(types)

        # سریالایزر برای داده‌های گروه‌بندی شده
        serializer = CategoryTypeSerializer(grouped_data, many=True)

        # بازگشت پاسخ با ساختار جدید
        return Response(serializer.data, content_type='application/json; charset=UTF-8')

    def group_by_category(self, product_types):
        # تابعی برای گروه‌بندی محصولات بر اساس دسته‌بندی
        grouped_data = defaultdict(lambda: {'category': '', 'cat_id': 0, 'types': []})

        for product in product_types:
            category_name = product.category.name
            category_id = product.category.id
            grouped_data[category_name]['category'] = category_name
            grouped_data[category_name]['cat_id'] = category_id
            grouped_data[category_name]['types'].append(product)

        return list(grouped_data.values())




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



class BazarWithOptionalSelBuyApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        sell_buy = request.GET.get('sell_buy')
        if sell_buy:
            all_bazar = Product.objects.filter(sell_buy=sell_buy, expire_time__gt=datetime.now())
        else:
            all_bazar = Product.objects.filter(expire_time__gt=datetime.now())

        all_bazar_serializer = ApiAllProductSerializer(all_bazar.order_by('price')[:100], many=True)
        return Response(all_bazar_serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')



class BazarWithOptionalSelBuyWebApi(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        sell_buy = request.GET.get('sell_buy')
        if sell_buy:
            all_bazar = Product.objects.filter(sell_buy=sell_buy, expire_time__gt=datetime.now())
        else:
            all_bazar = Product.objects.filter(expire_time__gt=datetime.now())

        all_bazar_serializer = ApiAllProductSerializer(all_bazar.order_by('price')[:100], many=True)
        return Response(all_bazar_serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')



class InBazarApi(APIView):

    def get(self, request, pk, *args, **kwargs):
        title = ProductType.objects.filter(pk=pk).first()
        title_serializer = ProductTypeSerializer(title)

        # Sellers: sorted by ascending price (lowest first)
        sellers = Product.objects.filter(sell_buy=1, product_type_id=pk, expire_time__gt=datetime.now())
        sellers_serializer = ProductSellSerializer(sellers.order_by('price')[:30], many=True)

        # Buyers: sorted by descending price (highest first)
        buyers = Product.objects.filter(sell_buy=2, product_type_id=pk, expire_time__gt=datetime.now())
        buyers_serializer = ProductSellSerializer(buyers.order_by('-price')[:30], many=True)

        context = {
            'title': title_serializer.data,
            'sellers': sellers_serializer.data,
            'buyers': buyers_serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)




class SellSingleBazarApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        product_serializer = SellSingleProductSerializer(product)

        return Response(product_serializer.data, status=status.HTTP_200_OK)


class BuySingleBazarApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        product_serializer = BuySingleProductSerializer(product)

        return Response(product_serializer.data, status=status.HTTP_200_OK)



class BidSingleBazarApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(pk=pk).first()
        bids = product.bids.order_by('-price')
        bids_serializer = BidSerializer(bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)


class SellBidSingleBazarApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(pk=pk).first()
        bids = product.bids.order_by('-price')
        bids_serializer = BidSerializer(bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)



class BuyBidSingleBazarApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(pk=pk).first()
        bids = product.bids.order_by('price')
        bids_serializer = BidSerializer(bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)



class TypeByIdApi(APIView):
    def get(self, request, id, *args, **kwargs):
        type = ProductType.objects.filter(pk=id).first()

        type_serializer = ProductTypeSerializer(type)
        print(type_serializer.data)
        return Response(type_serializer.data, status=status.HTTP_200_OK)


class BidSellListApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"detail": "محصول پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)

        product_type = product.product_type
        # فیلتر کردن محصولاتی که در حال فروش هستند و بیدهایشان را با قیمت مرتب می‌کنیم
        products = Product.objects.filter(sell_buy=1, product_type=product_type).prefetch_related(
            Prefetch('bids', queryset=Bid.objects.order_by('-price'))
        )

        bids = []
        for prod in products:
            # افزودن تمام بیدها به لیست
            bids.extend(prod.bids.all())

        # مرتب‌سازی بیدها بر اساس قیمت پس از تجمیع در یک لیست
        sorted_bids = sorted(bids, key=lambda x: x.price, reverse=True)

        # محدود کردن لیست به 20 بید
        limited_bids = sorted_bids[:20]

        bids_serializer = BidSerializer(limited_bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)



class BidBuyListApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"detail": "محصول پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)

        product_type = product.product_type
        # فیلتر کردن محصولاتی که در حال فروش هستند و بیدهایشان را با قیمت مرتب می‌کنیم
        products = Product.objects.filter(sell_buy=2, product_type=product_type).prefetch_related(
            Prefetch('bids', queryset=Bid.objects.order_by('price'))
        )

        bids = []
        for prod in products:
            # افزودن تمام بیدها به لیست
            bids.extend(prod.bids.all())

        # مرتب‌سازی بیدها بر اساس قیمت پس از تجمیع در یک لیست
        sorted_bids = sorted(bids, key=lambda x: x.price, reverse=False)

        # محدود کردن لیست به 20 بید
        limited_bids = sorted_bids[:20]

        bids_serializer = BidSerializer(limited_bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)




class BidSellListChartApi(APIView):
    def get(self, request, pk, *args, **kwargs):

        product_type = pk
        # فیلتر کردن محصولاتی که در حال فروش هستند و بیدهایشان را با قیمت مرتب می‌کنیم
        products = Product.objects.filter(sell_buy=1, product_type=product_type).prefetch_related(
            Prefetch('bids', queryset=Bid.objects.order_by('-price'))
        )

        bids = []
        for prod in products:
            # افزودن تمام بیدها به لیست
            bids.extend(prod.bids.all())

        # مرتب‌سازی بیدها بر اساس قیمت پس از تجمیع در یک لیست
        sorted_bids = sorted(bids, key=lambda x: x.price, reverse=True)

        # محدود کردن لیست به 20 بید
        limited_bids = sorted_bids[:20]

        bids_serializer = BidSerializer(limited_bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)


class CategoryNameApi(APIView):
    def get(self, request, pk, *args, **kwargs):

        productType = ProductType.objects.filter(pk=pk).first()
        productType_serializer = ProductTypeSerializer(productType)
        return Response(productType_serializer.data, status=status.HTTP_200_OK)



class BidBuyListChartApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        product_type = pk
        # فیلتر کردن محصولاتی که در حال فروش هستند و بیدهایشان را با قیمت مرتب می‌کنیم
        products = Product.objects.filter(sell_buy=2, product_type=product_type).prefetch_related(
            Prefetch('bids', queryset=Bid.objects.order_by('price'))
        )

        bids = []
        for prod in products:
            # افزودن تمام بیدها به لیست
            bids.extend(prod.bids.all())

        # مرتب‌سازی بیدها بر اساس قیمت پس از تجمیع در یک لیست
        sorted_bids = sorted(bids, key=lambda x: x.price, reverse=False)

        # محدود کردن لیست به 20 بید
        limited_bids = sorted_bids[:20]

        bids_serializer = BidSerializer(limited_bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)



class BidSellListByTypeApi(APIView):
    def get(self, request, pk, *args, **kwargs):

        # فیلتر کردن محصولاتی که در حال فروش هستند و بیدهایشان را با قیمت مرتب می‌کنیم
        products = Product.objects.filter(sell_buy=1, product_type=pk).prefetch_related(
            Prefetch('bids', queryset=Bid.objects.order_by('-price'))
        )

        bids = []
        for prod in products:
            # افزودن تمام بیدها به لیست
            bids.extend(prod.bids.all())

        # مرتب‌سازی بیدها بر اساس قیمت پس از تجمیع در یک لیست
        sorted_bids = sorted(bids, key=lambda x: x.price, reverse=False)

        # محدود کردن لیست به 20 بید
        limited_bids = sorted_bids[:20]

        # سریال‌سازی بیدها
        bids_serializer = BidSerializer(limited_bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)



class BidBuyListByTypeApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        # فیلتر کردن محصولات با نوع خاص
        products = Product.objects.filter(sell_buy=2, product_type=pk).prefetch_related(
            Prefetch('bids', queryset=Bid.objects.order_by('price'))
        )

        bids = []
        for prod in products:
            # افزودن تمام بیدها به لیست
            bids.extend(prod.bids.all())

        # مرتب‌سازی بیدها بر اساس قیمت پس از تجمیع در یک لیست
        sorted_bids = sorted(bids, key=lambda x: x.price, reverse=True)

        # محدود کردن لیست به 20 بید
        limited_bids = sorted_bids[:20]

        # سریال‌سازی بیدها
        bids_serializer = BidSerializer(limited_bids, many=True, context={'request': request})

        return Response(bids_serializer.data, status=status.HTTP_200_OK)


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







class ApiProductCreateAPIViewV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]



    def post(self, request, *args, **kwargs):
        user = request.user

        # دریافت داده‌های فرم
        price = request.data.get('price')
        weight = request.data.get('weight')
        sell_buy_code = request.data.get('sell_buy')  # دریافت مقدار sell_buy
        warranty = request.data.get('warranty') == 'True'
        expire_time_days = request.data.get('expire_time')
        description = request.data.get('description')
        product_type_id = request.data.get('product_type')
        attrs = request.data.get('attrs')
        attrs = json.loads(attrs) if attrs else []

        # بررسی تاریخ انقضا
        if expire_time_days:
            expire_time = timezone.now() + timezone.timedelta(days=int(expire_time_days))
        else:
            expire_time = None



        # تبدیل مقدار sell_buy از عدد به متن
        if sell_buy_code == '1':
            sell_buy = Product.SELL
        else:
            sell_buy = Product.BUY

        # بررسی نوع محصول
        product_type = get_object_or_404(ProductType, id=product_type_id)

        # ذخیره محصول
        upc = random.randint(11111111111111111, 99999999999999999)
        product = Product(
            user=user,
            sell_buy=sell_buy,
            product_type=product_type,
            upc=upc,
            price=price,
            weight=weight,
            description=description,
            is_successful=True,
            warranty=warranty,
            is_active=True,  # محصول به صورت پیش‌فرض غیرفعال است
            expire_time=expire_time
        )
        product.save()

        # ذخیره تصاویر
        num_images = int(request.data.get('numpic', 0))

        for i in range(num_images):
            image = request.FILES.get(f'image{i}')
            if image:
                product_image = ProductImage(image=image, product=product)
                product_image.save()

        # ذخیره ویژگی‌های محصول
        for attr in attrs:
            attribute = get_object_or_404(ProductAttribute, id=attr['attr'])
            attribute_value = get_object_or_404(ProductAttributeValue, id=attr['value'])
            ProductAttr(type=product_type, attr=attribute, value=attribute_value, product=product).save()

        return Response({"status": "success", "message": "Product added successfully!"}, status=status.HTTP_201_CREATED)


class ChartByTypeIdApi(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        # گرفتن محصولات مربوط به product_type مورد نظر
        product_type = id

        # محصولات فعال که زمان انقضا آن‌ها نگذشته باشد
        products = Product.objects.filter(
            product_type_id=product_type,
            expire_time__gte=timezone.now(),  # محصولاتی که منقضی نشده‌اند
            is_active=True
        )

        # جمع‌بندی داده‌ها بر اساس تاریخ و نوع (sell یا buy)
        data_by_date = products.values('create_time__date', 'sell_buy').annotate(
            total_weight=Sum('weight'),  # مجموع وزن‌ها
            max_price=Max('price'),  # حداکثر قیمت
            min_price=Min('price')  # حداقل قیمت
        ).order_by('create_time__date')

        # آماده‌سازی داده‌ها برای نمودار
        chart_data = {}
        for entry in data_by_date:
            date_str = entry['create_time__date'].strftime('%Y-%m-%d')
            sell_buy_type = entry['sell_buy']

            if date_str not in chart_data:
                chart_data[date_str] = {
                    'maxPriceSell': 0,
                    'minPriceSell': 0,
                    'maxPriceBuy': 0,
                    'minPriceBuy': 0,
                    'volume': 0
                }

            # پر کردن داده‌ها بر اساس نوع فروش یا خرید
            if sell_buy_type == Product.SELL:
                chart_data[date_str]['maxPriceSell'] = entry['max_price']
                chart_data[date_str]['minPriceSell'] = entry['min_price']
                chart_data[date_str]['volume'] += entry['total_weight']  # اضافه‌کردن وزن فروش به حجم کل
            elif sell_buy_type == Product.BUY:
                chart_data[date_str]['maxPriceBuy'] = entry['max_price']
                chart_data[date_str]['minPriceBuy'] = entry['min_price']
                chart_data[date_str]['volume'] += entry['total_weight']  # اضافه‌کردن وزن خرید به حجم کل

        # آماده‌سازی داده‌های نهایی برای نمودار
        final_data = [
            {
                'date': date,
                'maxPriceSell': data['maxPriceSell'],
                'minPriceSell': data['minPriceSell'],
                'maxPriceBuy': data['maxPriceBuy'],
                'minPriceBuy': data['minPriceBuy'],
                'volume': data['volume']
            }
            for date, data in chart_data.items()
        ]

        # بازگرداندن داده‌ها به صورت JSON
        return Response(final_data, status=200)