import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import get_user_model as user_model
from django.contrib import messages
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from blog.models import Blog
from catalogue.models import Product
from catalogue.serializers import ProductSellSerializer
from company.forms import CompanyForm
from company.models import Company
from index.models import SettingApp
from index.serializers import SettingsSerializer
from info.forms import InfoUserForm, FarmerForm, ServiceForm, BrokerForm, StorageForm
from django.views.decorators.http import require_http_methods
from info.models import Info, Farmer
from info import forms
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from config.lib_custom.utils import CustomPagination
from learn.models import Learn
from transaction.models import Transaction
from transaction.views import add_balance_user
from config.lib_custom.get_info_by_user import GetInfoByUser


class MainAdmin(View):
    template_name = 'index/sharjewallet.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['products'] = Product.objects.filter(is_active=False).filter(expire_time__gt=datetime.datetime.now())
        context['info'] = Info.objects.filter(user=request.user).first()
        context['company'] = Company.objects.filter(user=request.user).first()
        form_info = InfoUserForm()
        context['form_info'] = form_info
        form_company = CompanyForm()
        context['form_company'] = form_company
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class MainIndex(View):
    template_name = 'web/index2.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['blogs'] = Blog.objects.filter(status=True).all()
        if request.user.is_anonymous:
            products = Product.objects.filter(is_active=True).filter(
                expire_time__gt=datetime.datetime.now()).order_by('price')
            context['products'] = products
            new_context = CustomPagination.create_paginator(products, 8, 3, context, request)
            context['paginator'] = new_context['paginator']
            context['page_obj'] = new_context['page_obj']
            context['limit_number'] = new_context['limit_number']
            context['num_pages'] = new_context['num_pages']

        else:
            products = Product.objects.filter(is_active=True).filter(
                expire_time__gt=datetime.datetime.now()).order_by('price')
            context['products'] = products
            context['info'] = Info.objects.filter(user=request.user).first()
            context['company'] = Company.objects.filter(user=request.user).first()
            form_info = InfoUserForm()
            context['form_info'] = form_info
            form_company = CompanyForm()
            context['form_company'] = form_company
            new_context = CustomPagination.create_paginator(products, 8, 3, context, request)
            context['paginator'] = new_context['paginator']
            context['page_obj'] = new_context['page_obj']
            context['limit_number'] = new_context['limit_number']
            context['num_pages'] = new_context['num_pages']

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class MainIndexSearch(View):
    template_name = 'web/search/index.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        sbazar = request.GET.get('bazar')
        stype = request.GET.get('type')
        sprice = request.GET.get('price')
        if sbazar == "None":
            sbazar = None
            tbazar = False
        else:
            tbazar = True

        if stype == "None":
            stype = None
            ttype = False
        else:
            ttype = True

        if sprice == "None":
            sprice = None
            tprice = False
        else:
            tprice = True

        if tbazar:
            if ttype:
                if tprice:
                    text = "همه پر هستند"
                    allproducts = Product.objects.filter(is_active=True)\
                        .filter(expire_time__gt=datetime.datetime.now())\
                        .filter(sell_buy=sbazar)\
                        .filter(product_type=stype)
                else:
                    text = "فقط مبلغ خالیه"
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(sell_buy=sbazar) \
                        .filter(product_type=stype)
            else:
                if tprice:
                    text = "نوع خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(sell_buy=sbazar)
                else:
                    text = "نوع و قیمت خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(sell_buy=sbazar)
        else:
            if ttype:
                if tprice:
                    text = "بازار خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(product_type=stype)
                else:
                    text = "بازار و قیمت خالی هستند "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(product_type=stype)
            else:
                if tprice:
                    text = "بازار و نوع خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now())
                else:
                    text = "بازار و نوع و مبلغ خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now())

        if request.user.is_anonymous:

            if sprice == "low":
                context['products'] = allproducts.order_by('price')
            if sprice == "top":
                context['products'] = allproducts.order_by('-price')
            else:
                context['products'] = allproducts
        else:
            if sprice == "low":
                context['products'] = allproducts.order_by('price')
            if sprice == "top":
                context['products'] = allproducts.order_by('-price')
            else:
                context['products'] = allproducts

            products = context['products']
            context['info'] = Info.objects.filter(user=request.user).first()
            context['company'] = Company.objects.filter(user=request.user).first()
            form_info = InfoUserForm()
            context['form_info'] = form_info
            form_company = CompanyForm()
            context['form_company'] = form_company
            new_context = CustomPagination.create_paginator(products, 8, 3, context, request)
            context['paginator'] = new_context['paginator']
            context['page_obj'] = new_context['page_obj']
            context['limit_number'] = new_context['limit_number']
            context['num_pages'] = new_context['num_pages']

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class BazarApiSearch(APIView):
    def post(self, request, *args, **kwargs):
        # دریافت بدنه‌ی درخواست و تبدیل آن به دیکشنری
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=400)

        # دریافت پارامترها از درخواست و مدیریت مقادیر "None" به عنوان رشته
        sbazar = body.get('bazar')
        stype = body.get('type')
        sprice = body.get('price')
        page_number = body.get('page', 1)

        # تبدیل مقادیر رشته‌ای "None" به None
        sbazar = None if sbazar == "None" else sbazar
        stype = None if stype == "None" else stype
        sprice = None if sprice == "None" else sprice

        # اطمینان از اینکه شماره صفحه به صورت عدد صحیح است
        try:
            page_number = int(page_number)
        except ValueError:
            return Response({"error": "Page number must be an integer"}, status=400)

        print(f"Received params: bazar={sbazar}, type={stype}, price={sprice}, page={page_number}")

        # ایجاد فیلتر اولیه
        filters = Q(is_active=True) & Q(expire_time__gt=timezone.now())

        # اضافه کردن فیلتر برای sell_buy تنها در صورتی که مقدار آن None نباشد
        if sbazar is not None:
            filters &= Q(sell_buy=sbazar)

        # اضافه کردن فیلتر برای product_type تنها در صورتی که مقدار آن None نباشد
        if stype is not None:
            filters &= Q(product_type=stype)

        # گرفتن تمام محصولات با فیلترهای اعمال شده
        all_products = Product.objects.filter(filters)
        print(f"Total products after filters: {all_products.count()}")

        # مرتب‌سازی محصولات بر اساس قیمت
        if sprice == "low":
            products = all_products.order_by('price', 'id')  # اضافه کردن 'id' برای اطمینان از ترتیب ثابت
        elif sprice == "top":
            products = all_products.order_by('-price', 'id')  # اضافه کردن 'id' برای اطمینان از ترتیب ثابت
        else:
            products = all_products.order_by('id')  # ترتیب پیش‌فرض بر اساس شناسه

        # تنظیم صفحه‌بندی
        paginator = PageNumberPagination()
        paginator.page_size = 12

        # تنظیم شماره صفحه
        request.query_params._mutable = True
        request.query_params['page'] = page_number
        request.query_params._mutable = False

        # صفحه‌بندی بر اساس شماره صفحه دریافتی
        result_page = paginator.paginate_queryset(products, request)
        print(f"Paginator page size: {paginator.page_size}")
        print(f"Paginator current page: {page_number}")
        print(f"Result page count: {paginator.page.paginator.num_pages}")
        print(f"Result page items count: {len(result_page)}")

        # سریالایز کردن محصولات و برگرداندن پاسخ
        serializer = ProductSellSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get(self, request, *args, **kwargs):
        context = dict()
        sbazar = request.GET.get('bazar')
        stype = request.GET.get('type')
        sprice = request.GET.get('price')
        if sbazar == "None":
            sbazar = None
            tbazar = False
        else:
            tbazar = True

        if stype == "None":
            stype = None
            ttype = False
        else:
            ttype = True

        if sprice == "None":
            sprice = None
            tprice = False
        else:
            tprice = True

        if tbazar:
            if ttype:
                if tprice:
                    text = "همه پر هستند"
                    allproducts = Product.objects.filter(is_active=True)\
                        .filter(expire_time__gt=datetime.datetime.now())\
                        .filter(sell_buy=sbazar)\
                        .filter(product_type=stype)
                else:
                    text = "فقط مبلغ خالیه"
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(sell_buy=sbazar) \
                        .filter(product_type=stype)
            else:
                if tprice:
                    text = "نوع خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(sell_buy=sbazar)
                else:
                    text = "نوع و قیمت خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(sell_buy=sbazar)
        else:
            if ttype:
                if tprice:
                    text = "بازار خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(product_type=stype)
                else:
                    text = "بازار و قیمت خالی هستند "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now()) \
                        .filter(product_type=stype)
            else:
                if tprice:
                    text = "بازار و نوع خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now())
                else:
                    text = "بازار و نوع و مبلغ خالی است "
                    allproducts = Product.objects.filter(is_active=True) \
                        .filter(expire_time__gt=datetime.datetime.now())

        if request.user.is_anonymous:

            if sprice == "low":
                context['products'] = allproducts.order_by('price')
            if sprice == "top":
                context['products'] = allproducts.order_by('-price')
            else:
                context['products'] = allproducts
        else:
            if sprice == "low":
                context['products'] = allproducts.order_by('price')
            if sprice == "top":
                context['products'] = allproducts.order_by('-price')
            else:
                context['products'] = allproducts

            products = context['products']
            context['info'] = Info.objects.filter(user=request.user).first()
            context['company'] = Company.objects.filter(user=request.user).first()
            form_info = InfoUserForm()
            context['form_info'] = form_info
            form_company = CompanyForm()
            context['form_company'] = form_company
            new_context = CustomPagination.create_paginator(products, 8, 3, context, request)
            context['paginator'] = new_context['paginator']
            context['page_obj'] = new_context['page_obj']
            context['limit_number'] = new_context['limit_number']
            context['num_pages'] = new_context['num_pages']


        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class Profile(View):
    template_name = 'web/profile/update_info/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class ProfileEtc(View):
    template_name = 'web/profile/etc_info/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)
        farmer = Farmer.objects.filter(user=request.user).first()
        context['farmer'] = farmer
        if farmer:
            context['ok_ok'] = 1
        else:
            context['ok_ok'] = 0
        form_farmer = FarmerForm()
        context['form_farmer'] = form_farmer
        form_storage = StorageForm()
        context['form_storage'] = form_storage
        form_broker = BrokerForm()
        context['form_broker'] = form_broker
        form_service = ServiceForm()
        context['form_service'] = form_service

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class ProfileProduct(View):
    template_name = 'web/profile/product/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class ProfileRequestMain(View):
    template_name = 'web/profile/product/request.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class ProfileRequest(View):
    template_name = 'web/profile/product/index_request.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class ProfileLearn(View):
    template_name = 'web/profile/learn/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class ProfileWallet(View):
    template_name = 'web/profile/transaction/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class MainProduct(View):
    template_name = 'web/profile/product/main.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class MainRequest(View):
    template_name = 'web/profile/product/request.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = GetInfoByUser.get_all_info_by_user(request)
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)

@login_required
@require_http_methods(request_method_list=['POST'])
def update_user(request):
    mobile = request.user.mobile
    User = user_model()
    user = User.objects.filter(mobile=mobile).first()


    if request.POST['name'] != '':
        user.first_name = request.POST['name']
        user.save()
    if request.POST['family'] != '':
        user.last_name = request.POST['family']
        user.save()
    if request.POST['email'] != '':
        user.email = request.POST['email']
        user.save()

    messages.success(request, "اطلاعات بروزرسانی شد!")
    return HttpResponseRedirect(reverse_lazy('profile'))


@login_required
@require_http_methods(request_method_list=['POST'])
def update_info(request):
    checkoneuser = request.user
    infoexist = Info.objects.filter(user_id=checkoneuser.pk).first()
    if infoexist:
        form = forms.InfoUserForm(request.POST, request.FILES, instance=infoexist)
    else:
        form = forms.InfoUserForm(request.POST, request.FILES)

    if form.is_valid():
        information = form.save(commit=False)
        if infoexist:

            information.save()
        else:

            information.user = request.user
            information.is_active = False
            information.save()
        messages.info(request, "اطلاعات با موفقیت ارسال شد، بعد از تایید اطلاعات می توانید از این سامانه استفاده کنید")
        return HttpResponseRedirect(reverse_lazy('profile'))
    else:
        if request.POST.get('codemeli') == 'None':
            return HttpResponseRedirect(reverse_lazy('profile'))
        if not testmeli(request.POST.get('codemeli'))[1]:
            messages.error(request, testmeli(request.POST.get('codemeli'))[0])
            return HttpResponseRedirect(reverse_lazy('profile'))

        if request.POST.get('shaba') is not None:
            if not testshaba(request.POST.get('shaba'))[1]:
                messages.error(request, testshaba(request.POST.get('shaba'))[0])
                return HttpResponseRedirect(reverse_lazy('profile'))
    messages.error(request, "اطلاعات ارسال شده توسط شما مطابق انتظار ما نبود! لطفا مجددا تلاش نمائید")
    return HttpResponseRedirect(reverse_lazy('profile'))


def testshaba(shaba):
    res = True
    message_error = "در حال بررسی شبای بانکی ..."
    if shaba == "None":
        message_error = None
        res = False
        return message_error, res
    if len(shaba) != 24:
        message_error = "شماره شبا وارد شده معتبر نیست"
        res = False
        return message_error, res
    existshaba = Info.objects.filter(shaba=shaba).first()
    if existshaba:
        message_error = "شماره شبا وارد شده قبلا ثبت شده است"
        res = False
    return message_error, res


def testmeli(codemeli):
    res_meli = True
    message_error_meli = "در حال بررسی کد ملی ..."
    if len(codemeli) != 10:
        message_error_meli = "کد ملی وارد شده معتبر نیست"
        res_meli = False
        return message_error_meli, res_meli
    existmelli = Info.objects.filter(codemeli=codemeli).first()
    if existmelli:
        message_error_meli = "کد ملی وارد شده قبلا ثبت شده است"
        res_meli = False
    return message_error_meli, res_meli


@login_required
@require_http_methods(request_method_list=['POST'])
def update_info_image(request):
    check_one_user = request.user
    if check_one_user:

        form = forms.ProfileImageForm(request.POST, request.FILES, instance=check_one_user)
    else:

        form = forms.ProfileImageForm(request.POST, request.FILES)
    if form.is_valid():
        information = form.save(commit=False)
        information.image = request.FILES.get('image_info')
        information.save()
    return HttpResponseRedirect(reverse_lazy('profile'))


class Api(View):
    template_name = 'api/index.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['api_login'] = "api_login"
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class SettingsApi(APIView):
    @staticmethod
    def get(*args, **kwargs):
        settings = SettingApp.objects.first()
        serializer = SettingsSerializer(settings)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')