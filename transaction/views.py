from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from jalali_date import datetime2jalali, date2jalali
from django.views import View
from info.models import Info
from order.models import Payment
from order.utils import zpal_request_handler
from transaction.models import Transaction, UserBalance, TransferTransaction, UserScore
from transaction.utils import check_is_active, check_is_ok
from django.contrib import messages
from django.contrib.auth import get_user_model as user_model
from num2words import num2words
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json



def transaction_list(request):
    return HttpResponse("transaction list")


def get_report(request):
    users = Transaction.get_report()

    for user in users:
        context = ''.join(f"balance is : {user.balance} - and num transaction is : {user.transaction_count}")

    return HttpResponse(context)


@login_required
@user_passes_test(check_is_active)
def wallet(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        list = Transaction.get_list_transaction_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['transaction_list'] = list
        return render(request, 'ecommerce/wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def wallet_web(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        list = Transaction.get_list_transaction_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['transaction_list'] = list
        return render(request, 'ecommerce/web/wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def wallet_user(request, pk):

    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        list = Transaction.get_list_transaction_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['transaction_list'] = list
        return render(request, 'web/profile/wallet/index.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def list_send_wallet(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        list = TransferTransaction.get_list_transfer_transaction_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['transaction_list'] = list
        return render(request, 'ecommerce/list_send_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def list_send_wallet_web(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        list = TransferTransaction.get_list_transfer_transaction_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['transaction_list'] = list
        return render(request, 'ecommerce/web/list_send_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def list_received_wallet(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        list = TransferTransaction.get_received_list_transfer_transaction_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['transaction_list'] = list
        return render(request, 'ecommerce/list_received_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def list_received_wallet_web(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        list = TransferTransaction.get_received_list_transfer_transaction_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['transaction_list'] = list
        return render(request, 'ecommerce/web/list_received_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def add_wallet(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['loop_times'] = range(1, 8)
        return render(request, 'ecommerce/add_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def add_wallet_web(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        context['loop_times'] = range(1, 8)
        return render(request, 'ecommerce/web/sharjewallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def send_wallet(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']

        return render(request, 'ecommerce/send_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def send_wallet_web(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        userbalance = user['balance']
        print("userbalance")
        print(userbalance)
        context['balance'] = userbalance
        context['transaction_count'] = user['transaction_count']
        if userbalance > 1000000:
            return render(request, 'ecommerce/web/send_wallet.html', context=context)
        else:
            messages.error(request,
                           "کیف پول شما کمتر از یکصد هزار تومان است، ابتدا می بایست کیف پول خود را شارژ نمائید")
            return HttpResponseRedirect(reverse_lazy('add-wallet-by-user-web', kwargs={'pk': pk}))
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


# inja paaeeen bayad bere be samte dargahe pardakht
@login_required
@user_passes_test(check_is_active)
def form_add_wallet(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user = Transaction.get_report_by_user(pk)
        context['balance'] = user['balance']
        context['transaction_count'] = user['transaction_count']
        information = request.POST
        my_mobile = request.user.mobile
        amount = information['price']
        amount = int(amount)/10
        print(int(amount)/10)
        print(type(amount))
        payment_link, authority = zpal_request_handler(settings.ZARRINPAL['merchant_id'], amount,
                             "Wallet charge", None, my_mobile, settings.ZARRINPAL['gateway_callback_url'])

        print("******************************authority*************************************")
        print(authority)
        Payment.create_payment(authority, amount, request.user)
        print("******************************authority*************************************")

        if payment_link is not None:
            return redirect(payment_link)

        return render(request, 'ecommerce/send_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


# inja paaeeen bayad dar sorate mojodi kafi enteghal anjam migirad
@login_required
@user_passes_test(check_is_active)
def check_mobile_wallet(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user33 = Transaction.get_report_by_user(pk)
        context['balance'] = user33['balance']
        information = request.POST
        mobile_reciver = information['mobile']
        my_mobile = request.user.mobile
        if mobile_reciver == my_mobile:
            messages.error(request, "شما نمی توانید به خودتان اعتبار هدیه دهید!")
            return render(request, 'ecommerce/send_wallet.html', context=context)
        request.session['mob_receiver'] = mobile_reciver
        amount = information['price']
        request.session['amount_receiver'] = amount
        User = user_model()
        user_exist = User.objects.filter(mobile=mobile_reciver)

        if user_exist:
            user_exist = user_exist.first()
            user_pk_reciver = user_exist.pk
            user_info = Info.objects.filter(user_id=user_pk_reciver).first()
            context['mobile'] = mobile_reciver
            context['amount'] = amount
            context['name'] = user_info.name
            context['family'] = user_info.family

            return render(request, 'ecommerce/check_mobile_reciver_wallet.html', context=context)

        else:
            messages.error(request,
                           "کاربر دریافت کننده مد نظر شما در ربو وجود ندارد "
                           "و یا شماره موبایل وارد شده توسط شما صحیح نمی باشد!")
            return render(request, 'ecommerce/send_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


# inja paaeeen bayad dar sorate mojodi kafi enteghal anjam migirad
@login_required
@user_passes_test(check_is_active)
def check_mobile_wallet_web(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        user33 = Transaction.get_report_by_user(pk)
        context['balance'] = user33['balance']
        information = request.POST
        mobile_reciver = information['mobile']
        my_mobile = request.user.mobile
        if mobile_reciver == my_mobile:
            messages.error(request, "شما نمی توانید به خودتان اعتبار هدیه دهید!")
            return render(request, 'ecommerce/send_wallet.html', context=context)
        request.session['mob_receiver'] = mobile_reciver
        amount = information['price']
        request.session['amount_receiver'] = amount
        User = user_model()
        user_exist = User.objects.filter(mobile=mobile_reciver)

        if user_exist:
            user_exist = user_exist.first()
            user_pk_reciver = user_exist.pk
            user_info = Info.objects.filter(user_id=user_pk_reciver).first()
            context['mobile'] = mobile_reciver
            context['amount'] = amount
            context['name'] = user_info.name
            context['family'] = user_info.family

            return render(request, 'ecommerce/web/check_mobile_reciver_wallet.html', context=context)

        else:
            messages.error(request,
                           "کاربر دریافت کننده مد نظر شما در ربو وجود ندارد "
                           "و یا شماره موبایل وارد شده توسط شما صحیح نمی باشد!")
            return render(request, 'ecommerce/web/send_wallet.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


# inja paaeeen bayad dar sorate mojodi kafi enteghal anjam migirad
@login_required
@user_passes_test(check_is_active)
def form_send_wallet(request, pk):
    if check_is_ok(request.user, pk):
        context = dict()
        information = request.POST
        mobile_reciver = information['mobile']
        amount = information['price']
        session_mobile = request.session.get('mob_receiver')
        session_amount = request.session.get('amount_receiver')
        if mobile_reciver == session_mobile:
            if amount == session_amount:
                result = TransferTransaction.transfer(pk, mobile_reciver, amount)
                context['result'] = result
                messages.info(request, "انتقال با موفقیت انجام شد!")
                request.session['mob_receiver'] = None
                request.session['amount_receiver'] = None
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                messages.error(request, "قیمت شما تغییر پیدا کرد لطفا دوباره از ابتدا تلاش کنید!")
                request.session['mob_receiver'] = None
                request.session['amount_receiver'] = None
                return HttpResponseRedirect(reverse_lazy('index'))
        else:
            messages.error(request, "موبایل دریافت کننده تغییر پیدا کرد لطفا دوباره از ابتدا تلاش کنید!")
            request.session['mob_receiver'] = None
            request.session['amount_receiver'] = None
            return HttpResponseRedirect(reverse_lazy('index'))

    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


def add_balance_user(request, pk):
    result = UserBalance.record_user_by_id_balance(pk)

    return HttpResponse(f"add balance by user : {pk} ---- {result} ")


def add_balance_all_user(request):
    UserBalance.record_all_user_balance()
    return HttpResponse(f"add balance all user result")


def transfer_transaction(request, sender, receiver, amount):
    TransferTransaction.transfer(sender, receiver, amount)
    return HttpResponse("ok")


def add_score_user(request, pk, score):
    instance = UserScore.user_score(pk, score)
    return HttpResponse(instance)


@csrf_exempt
def number_to_farsi(request):
    if request.is_ajax():
        price = request.POST.get('price')
        price = int(price)

        price = num2words(price, lang='fa')
        tarjome = price
        return JsonResponse({'msg': tarjome})

