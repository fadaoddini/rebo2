from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model as user_model
from info import forms
from info.forms import ServiceForm, BrokerForm, StorageForm, FarmerForm
from info.models import Info, Farmer
from login.models import MyUser
from transaction.models import Transaction
from transaction.views import add_balance_user


def info(request):
    context = dict()
    context['user'] = User.objects.all()

    return render(request, 'index/sharjewallet.html', context=context)


@login_required
@require_http_methods(request_method_list=['POST'])
def update_info(request):
    mobile = request.user.mobile

    user = MyUser.objects.filter(mobile=mobile).first()
    transaction = Transaction(user=user, transaction_type=1, amount=0)
    transaction.save()
    add_balance_user(request, user.pk)
    form = forms.InfoUserForm(request.POST, request.FILES)
    if form.is_valid():
        information = form.save(commit=False)
        information.user = request.user
        information.is_active = False
        information.save()

        return HttpResponseRedirect(reverse_lazy('index'))

    messages.error(request, "اطلاعات ارسال شده توسط شما مطابق انتظار ما نبود! لطفا مجددا تلاش نمائید")
    return HttpResponseRedirect(reverse_lazy('index'))


def add_service(request, *args, **kwargs):
    form = ServiceForm(request.POST, request.FILES)
    if form.is_valid():
        service = form.save(commit=False)
        service.user = request.user
        service.save()
        messages.info(request, "اطلاعات خدمات دهنده با موفقیت ثبت شد")
    else:
        messages.error(request, "با خطا روبرو شد!")
    return HttpResponseRedirect(reverse_lazy('profile'))


def add_broker(request, *args, **kwargs):
    form = BrokerForm(request.POST, request.FILES)
    if form.is_valid():
        broker = form.save(commit=False)
        broker.user = request.user
        broker.save()
        messages.info(request, "اطلاعات معامله گر با موفقیت ثبت شد")
    else:
        messages.error(request, "با خطا روبرو شد!")
    return HttpResponseRedirect(reverse_lazy('profile'))


def add_storage(request, *args, **kwargs):
    form = StorageForm(request.POST, request.FILES)
    if form.is_valid():
        storage = form.save(commit=False)
        storage.user = request.user
        storage.save()
        messages.info(request, "اطلاعات سردخانه با موفقیت ثبت شد")
    else:
        messages.error(request, "با خطا روبرو شد!")
    return HttpResponseRedirect(reverse_lazy('profile'))


def add_farmer(request, *args, **kwargs):
    farmer_exist = Farmer.objects.filter(user=request.user).first()
    if farmer_exist:
        messages.info(request, "اطلاعات کشاورز قبل تر موجود است")
        return HttpResponseRedirect(reverse_lazy('profile'))

    form = FarmerForm(request.POST, request.FILES)
    if form.is_valid():
        lat = request.POST['lat']
        long = request.POST['long']
        new_lat = round(float(lat), 6)
        new_long = round(float(long), 6)
        print('new_lat')
        print(new_lat)
        print(new_long)
        print('new_long')
        farmer = form.save(commit=False)
        farmer.user = request.user
        farmer.lat = new_lat
        farmer.long = new_long
        farmer.save()
        messages.info(request, "اطلاعات کشاورز با موفقیت ثبت شد")
    else:
        messages.error(request, "با خطا روبرو شد!")
    return HttpResponseRedirect(reverse_lazy('profile'))
