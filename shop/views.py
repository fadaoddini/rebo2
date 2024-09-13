import random

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
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework_simplejwt.authentication import JWTAuthentication
from shop import models, forms
from shop.models import Product, Location, MyShop, ProductImage, Package, Category
from django.contrib.auth import get_user_model as user_model
from cart.forms import CartAddProductForm
from shop.serializers import MyShopSerializer, ProductShopSerializer, PackageSerializer, CategorySerializer


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


class MyShopApi(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']
        my_shop = MyShop.objects.filter(pk=id).first()
        serializer = MyShopSerializer(my_shop, many=False)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class AllShopApi(APIView):
    def get(self, request, *args, **kwargs):
        context = dict()
        shops = MyShop.objects.filter(is_active=True).all()
        serializer = MyShopSerializer(shops, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class AddShopApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # بررسی اگر کاربر قبلاً فروشگاهی ثبت کرده باشد
        if MyShop.objects.filter(user=request.user).exists():
            return Response({"error": "شما قبلاً یک فروشگاه ثبت کرده‌اید."}, status=HTTP_400_BAD_REQUEST)

        # اگر فروشگاهی ثبت نشده باشد، می‌توانید آن را ایجاد کنید
        serializer = MyShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CheckUserShopApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            shop = MyShop.objects.get(user=request.user)
            serializer = MyShopSerializer(shop)
            return Response({"shop_exists": True, "shop": serializer.data}, status=HTTP_200_OK)
        except MyShop.DoesNotExist:
            return Response({"shop_exists": False}, status=HTTP_200_OK)


class PackageListApi(APIView):
    def get(self, request, *args, **kwargs):
        packages = Package.objects.all()
        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data)


class CategoryListApi(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True)  # فقط والدین
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ChildCategoryListApi(APIView):
    def get(self, request, parent_id, *args, **kwargs):
        categories = Category.objects.filter(parent_id=parent_id)  # فقط فرزندان
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class AddProductApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("ما در حال تست افزودن محصول در فروشگاه هستیم ")
        user = request.user
        data = request.data

        # بررسی وجود فروشگاه برای کاربر
        try:
            my_shop = MyShop.objects.get(user=user)
        except MyShop.DoesNotExist:
            return Response({"detail": "User does not have a shop."}, status=HTTP_400_BAD_REQUEST)
        print("داده‌های دریافتی:", request.data)  # چاپ داده‌های دریافتی
        print("data.get('sub_category')")
        print(data.get('subCategory'))
        print("data.get('sub_category')")
        # ایجاد محصول جدید با داده‌های دریافتی
        new_product = Product(
            user=user,
            category_id=data.get('category'),
            sub_category_id=data.get('subCategory'),
            my_shop=my_shop,
            title=data.get('title'),
            package_id=data.get('package'),
            upc=str(random.randint(10 ** 15, 10 ** 16 - 1)),
            price=int(data.get('price')),  # تبدیل به عدد صحیح
            discount=int(data.get('discount')),  # تبدیل به عدد صحیح
            weight=int(data.get('weight')),  # تبدیل به عدد صحیح
            description=data.get('description'),
            number_exist=int(data.get('number_exist')),  # تبدیل به عدد صحیح
            number_send=int(data.get('number_send'))  # تبدیل به عدد صحیح
        )

        new_product.save()

        # بارگذاری تصاویر محصول
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(image=image, product=new_product)

        serializer = ProductShopSerializer(new_product)
        return Response(serializer.data, status=HTTP_201_CREATED)


class EditProductApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, product_id, *args, **kwargs):
        print("product_id :")
        print(product_id)
        print("ما در حال ویرایش محصول در فروشگاه هستیم")
        user = request.user
        data = request.data
        category = data.get('category')
        subCategory = data.get('subCategory')
        package = data.get('package')
        print("=====================================================================")
        print(category)
        print(subCategory)
        print(package)
        print("=====================================================================")
        print("داده‌های دریافتی:", request.data)
        print("تصاویر دریافتی:", request.FILES)
        # بررسی وجود فروشگاه برای کاربر
        try:
            my_shop = MyShop.objects.get(user=user)
        except MyShop.DoesNotExist:
            return Response({"detail": "User does not have a shop."}, status=HTTP_400_BAD_REQUEST)
        print("کاربر مورد تائید است")
        # بررسی وجود محصول
        try:
            product = Product.objects.get(id=product_id, my_shop=my_shop)
        except Product.DoesNotExist:
            return Response({"detail": "Product does not exist or doesn't belong to the user."}, status=HTTP_404_NOT_FOUND)
        print("محصول مورد تائید است")
        # بروزرسانی داده‌های محصول
        product.category_id = data.get('category', product.category_id)
        product.sub_category_id = data.get('subCategory', product.sub_category_id)
        product.title = data.get('title', product.title)
        product.package_id = data.get('package', product.package_id)
        product.price = int(data.get('price', product.price))  # تبدیل به عدد صحیح
        product.discount = int(data.get('discount', product.discount))  # تبدیل به عدد صحیح
        product.weight = int(data.get('weight', product.weight))  # تبدیل به عدد صحیح
        product.description = data.get('description', product.description)
        product.number_exist = int(data.get('number_exist', product.number_exist))  # تبدیل به عدد صحیح
        product.number_send = int(data.get('number_send', product.number_send))  # تبدیل به عدد صحیح
        product.is_active = False

        product.save()
        print("ذخیره شد")
        # بروزرسانی تصاویر محصول (در صورت ارسال تصاویر جدید)
        images = request.FILES.getlist('images')
        if images:
            # حذف تصاویر قدیمی مرتبط با محصول
            ProductImage.objects.filter(product=product).delete()
            # ذخیره تصاویر جدید
            for image in images:
                ProductImage.objects.create(image=image, product=product)
        print("تصاویر ذخیره شد")
        serializer = ProductShopSerializer(product)
        return Response(serializer.data, status=HTTP_200_OK)


class InactiveProductsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_active=False)
        serializer = ProductShopSerializer(products, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class ActiveProductsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        serializer = ProductShopSerializer(products, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class FeaturedProductsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(vije=True)
        serializer = ProductShopSerializer(products, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class AllProductsShopsApi(APIView):
    def get(self, request, *args, **kwargs):
        context = dict()
        products = Product.objects.filter(is_active=True).all()
        serializer = ProductShopSerializer(products, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')




