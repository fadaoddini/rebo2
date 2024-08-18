import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import transaction as tran2
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from login import forms, helper
from login.models import MyUser
from login.serializers import MyUserSerializer
from transaction.models import Transaction
from transaction.views import add_balance_user


def verify_otp(request):
    try:
        context = dict()
        mobile = request.session.get('user_mobile')
        user = MyUser.objects.get(mobile=mobile)
        if request.method == "POST":
            # check otp expiration
            if not helper.check_otp_expiration(mobile):
                messages.error(request, "کد شما اعتبار زمانی خود را از دست داده است لطفا مجددا سعی نمائید!")
                return HttpResponseRedirect(reverse_lazy('login-mobile'))
            if user.otp != int(request.POST.get('otp')):
                messages.error(request, "در وارد کردن کد ارسال شده بیشتر دقت کنید گویا اشتباه وارد می کنید!")
                return HttpResponseRedirect(reverse_lazy('login-mobile'))
            user.is_active = True
            user.save()
            login(request, user)
            if user.is_active is True:
                return HttpResponseRedirect(reverse_lazy('index'))
            return HttpResponseRedirect(reverse_lazy('profile'))
        context['mobile'] = mobile
        return render(request, 'login/verify.html', context=context)
    except MyUser.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy('login-mobile'))


def register_user(request):
    print("A")
    if request.user.is_authenticated:
        messages.info(request, "کاربر گرامی خوش آمدید!")
        return HttpResponseRedirect(reverse_lazy('index'))
    form = forms.RegisterUser
    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                print("B")

                user = MyUser.objects.get(mobile=mobile)
                # check otp exists
                if helper.check_otp_expiration(mobile):
                    messages.error(request, "شما به تازگی پیامکی دریافت نموده اید و هنوز کد شما معتبر است!")
                    return HttpResponseRedirect(reverse_lazy('verify-otp'))
                # send otp
                otp = helper.create_random_otp()
                helper.send_otp(mobile, otp)
                # save otp
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                # redirect to verify code
                return HttpResponseRedirect(reverse_lazy('verify-otp'))
        except MyUser.DoesNotExist:
            print("C")
            form = forms.RegisterUser(request.POST)
            print("formform.is_valid()")
            print(form.is_valid())
            print("form.is_valid()")
            if form.is_valid():
                print("D")
                with tran2.atomic():
                    user = form.save(commit=False)
                    # send otp
                    otp = helper.create_random_otp()
                    helper.send_otp(mobile, otp)
                    # save otp
                    user.otp = otp
                    user.is_active = False
                    user.save()
                    # sharje hadye sabtenam
                    transaction = Transaction(user=user, transaction_type=1, amount=200000)
                    transaction.save()
                    add_balance_user(request, user.pk)
                    request.session['user_mobile'] = user.mobile
                    return HttpResponseRedirect(reverse_lazy('verify-otp'))
    return render(request, 'login/login.html', {'form': form})


class SendOtp(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        mobile = body['mobile']

        messege = "کد تایید با موفقیت ارسال شد"
        status = "ok"
        user = MyUser.objects.filter(mobile=mobile)
        if user.exists():
            user = user.first()
            # check otp exists
            if helper.check_otp_expiration(mobile):
                messege = "شما به تازگی پیامکی دریافت نموده اید و هنوز کد شما معتبر است!"
                status = "failed"
            # send otp
            otp = helper.create_random_otp()
            helper.send_otp(mobile, otp)
            # save otp
            user.otp = otp
            user.save()
            data = {
                    'id': user.id,
                    'status': status,
                    'messege': messege,
                    'mobile': user.mobile,
                }
            return Response(data, content_type='application/json; charset=UTF-8')
        else:
            messege = "ثبت نام شدید"
            status = "ok"
            user = MyUser.objects.create(
                mobile=mobile,
            )
            # send otp
            otp = helper.create_random_otp()
            helper.send_otp(mobile, otp)
            # save otp
            user.otp = otp
            user.is_active = False
            user.save()
            data = {
                'id': user.id,
                'status': status,
                'messege': messege,
                'mobile': user.mobile,
            }
            return Response(data, content_type='application/json; charset=UTF-8')


class VerifyCode(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        mobile = body['mobile']
        code = body['code']

        messege = "کد شما صحیح بود"
        status = "ok"
        user = MyUser.objects.filter(mobile=mobile)
        if user.exists():
            user = user.first()
            # res = get_tokens_for_user(mobile)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            if not helper.check_otp_expiration(mobile):
                messege = f"کد شما اعتبار زمانی خود را از دست داده است لطفا مجددا سعی نمائید!"
                status = "failed"
                refresh_token1 = "poooooch"
                access_token1 = "poooooch"
                data = {
                    'status': status,
                    'messege': messege,
                    'refresh_token': refresh_token1,
                    'access_token': access_token1,
                }
                return Response(data, content_type='application/json; charset=UTF-8')
            if user.otp != int(code):
                messege = f"در وارد کردن کد ارسال شده بیشتر دقت کنید گویا اشتباه وارد می کنید!"
                status = "failed"
                refresh_token1 = "poooooch"
                access_token1 = "poooooch"
                data = {
                    'status': status,
                    'messege': messege,
                    'refresh_token': refresh_token1,
                    'access_token': access_token1,
                }
                return Response(data)
            userid = user.pk
            user.is_active = True
            user.save()
            data = {
                'status': status,
                'messege': messege,
                'refresh_token': refresh_token,
                'access_token': access_token,
                'user_id': userid,
            }
            return Response(data, content_type='application/json; charset=UTF-8')

        else:
            messege = f"کاربری با اطلاعات فوق وجود ندارد!"
            status = "failed"
            refresh_token = "poooooch"
            access_token = "poooooch"
            data = {
                'status': status,
                'messege': messege,
                'refresh_token': refresh_token,
                'access_token': access_token
            }
            return Response(data, content_type='application/json; charset=UTF-8')


def logouti(request):
    # خروج کاربر
    logout(request)

    # حذف کوکی‌های توکن
    response = HttpResponseRedirect(reverse_lazy('index'))
    response.delete_cookie('accessToken')
    response.delete_cookie('refreshToken')

    # نمایش پیام خروج
    messages.info(request, "شما از سامانه خارج شدید")

    return response


class VerifyNameApi(APIView):
    def post(self, request, *args, **kwargs):
        body = request.data  # استفاده از request.data برای دسترسی به داده‌ها

        mobile = body.get('mobile')
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        password = body.get('password')

        # اگر فقط mobile داده شده باشد، چک کردن وجود کاربر
        if mobile and not (first_name or last_name or password):
            my_user = MyUser.objects.filter(mobile=mobile).first()
            if my_user:
                serializer = MyUserSerializer(my_user)
                return Response(serializer.data, content_type='application/json; charset=UTF-8')
            else:
                return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND,
                                content_type='application/json; charset=UTF-8')

        # اگر تمام پارامترها (mobile, first_name, last_name, password) داده شده باشند، بروزرسانی اطلاعات
        if mobile and first_name and last_name and password:
            my_user, created = MyUser.objects.get_or_create(mobile=mobile)
            my_user.first_name = first_name
            my_user.last_name = last_name
            my_user.set_password(password)  # تنظیم رمز عبور
            my_user.save()

            serializer = MyUserSerializer(my_user)
            return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=UTF-8')

        # اگر پارامترهای ورودی کامل نباشند
        return Response({'detail': 'Invalid parameters.'}, status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json; charset=UTF-8')