import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication  # مطمئن شوید که این پکیج را نصب کرده‌اید
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import messages
import requests

import jwt
from django.middleware.csrf import get_token
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import transaction as tran2
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from login import forms, helper
from login.models import MyUser, Follow, Address
from login.serializers import MyUserSerializer, AddressSerializer
from rebo import settings
from transaction.models import Transaction
from transaction.views import add_balance_user
from rest_framework.parsers import MultiPartParser, FormParser


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

    if request.user.is_authenticated:
        messages.info(request, "کاربر گرامی خوش آمدید!")
        return HttpResponseRedirect(reverse_lazy('index'))
    form = forms.RegisterUser
    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')

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

            form = forms.RegisterUser(request.POST)

            if form.is_valid():

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

        message = "کد تایید با موفقیت ارسال شد"
        status = "ok"
        wait_time = 0  # زمان انتظار

        # دریافت یا ایجاد کاربر
        user, created = MyUser.objects.get_or_create(mobile=mobile)

        if not created and helper.check_otp_expiration(user.mobile):
            message = "شما به تازگی پیامکی دریافت نموده‌اید و هنوز کد شما معتبر است!"
            status = "failed"

            # محاسبه زمان باقی‌مانده
            now = datetime.now()
            otp_time = user.otp_create_time
            diff_time = now - otp_time

            # زمان باقی‌مانده به ثانیه
            wait_time = 120 - diff_time.seconds if diff_time.seconds < 120 else 0
        else:
            # ارسال OTP
            otp = helper.create_random_otp()
            helper.send_otp(mobile, otp)
            # ذخیره OTP و به‌روزرسانی زمان ارسال
            user.otp = otp
            user.otp_create_time = datetime.now()  # Update OTP creation time
            user.save()

        data = {
            'id': user.id,
            'status': status,
            'message': message,
            'mobile': user.mobile,
            'wait_time': wait_time,  # اضافه کردن زمان انتظار به پاسخ
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




def logouti(request):
    # خروج کاربر
    logout(request)

    # حذف کوکی‌های توکن
    response = HttpResponseRedirect(reverse_lazy('index'))
    response.delete_cookie('accessToken')  # تغییر نام به access_token
    response.delete_cookie('access_token')  # تغییر نام به access_token

    response.delete_cookie('refreshToken')  # تغییر نام به refresh_token
    response.delete_cookie('refresh_token')  # تغییر نام به refresh_token


    # نمایش پیام خروج
    messages.info(request, "شما از سامانه خارج شدید")

    return response



class VerifyCodeV1(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        mobile = body['mobile']
        code = body['code']

        user = MyUser.objects.filter(mobile=mobile).first()
        if user:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            # بررسی انقضای کد OTP
            if not helper.check_otp_expiration(mobile):
                return JsonResponse({'status': 'failed', 'message': 'کد شما اعتبار زمانی خود را از دست داده است!'}, status=400)

            # بررسی صحت کد OTP
            if user.otp != int(code):
                return JsonResponse({'status': 'failed', 'message': 'در وارد کردن کد ارسال شده بیشتر دقت کنید!'}, status=400)

            # فعال‌سازی حساب کاربری
            user.is_active = True
            user.save()

            # دریافت CSRF token
            csrf_token = get_token(request)

            response = JsonResponse({
                'status': 'ok',
                'message': 'کد شما صحیح بود',
                'user_id': user.pk,
            })

            # محیط توسعه
            # response.set_cookie('accessToken', access_token, httponly=True, secure=False, samesite='Lax')
            # response.set_cookie('refreshToken', refresh_token, httponly=False, secure=False, samesite='Lax')
            # response.set_cookie('csrftoken', csrf_token, httponly=False, secure=False, samesite='Lax')

            # محیط پروداکشن
            response.set_cookie('accessToken', access_token, httponly=True, secure=False, samesite='Lax')
            response.set_cookie('refreshToken', refresh_token, httponly=False, secure=False, samesite='Lax')
            response.set_cookie('csrftoken', csrf_token, httponly=False, secure=False, samesite='Lax')

            return response
        else:
            return JsonResponse({'status': 'failed', 'message': 'کاربری با اطلاعات فوق وجود ندارد!'}, status=400)



class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        # دریافت Access Token از کوکی
        access_token = request.COOKIES.get('accessToken')
        refresh_token = request.COOKIES.get('refreshToken')

        if not access_token:
            raise AuthenticationFailed('Access token not found in cookies.')

        try:
            # بررسی اعتبار توکن دسترسی
            validated_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # اگر توکن دسترسی منقضی شده است
            if refresh_token:
                try:
                    # بررسی و decode توکن رفرش
                    refresh_decoded = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
                    # تولید یک توکن دسترسی جدید
                    new_access_token = jwt.encode({'user_id': refresh_decoded['user_id'], 'exp': datetime.utcnow() + timedelta(minutes=5)}, settings.SECRET_KEY, algorithm='HS256')

                    # ساختن response جدید و ست کردن کوکی
                    response = JsonResponse({'status': 'success', 'message': 'Token refreshed.'})

                    # توسعه
                    # response.set_cookie('accessToken', new_access_token, httponly=True, secure=False, samesite='Lax')


                    # پروداکشن
                    response.set_cookie('accessToken', new_access_token, httponly=False, secure=False, samesite='Lax')

                    # دوباره بررسی معتبر بودن توکن جدید
                    validated_token = jwt.decode(new_access_token, settings.SECRET_KEY, algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Refresh token has expired.')
                except jwt.InvalidTokenError:
                    raise AuthenticationFailed('Invalid refresh token.')
            else:
                raise AuthenticationFailed('Access token expired and refresh token not found.')

        # بازگرداندن کاربر و توکن معتبر
        return self.get_user(validated_token), validated_token



class CheckTokenView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # کاربر احراز هویت‌شده
        access_token = request.COOKIES.get('accessToken')
        refresh_token = request.COOKIES.get('refreshToken')


        # بررسی زمان انقضای توکن و رفرش آن
        try:
            # بررسی اعتبار توکن
            validated_token = JWTAuthentication().get_validated_token(access_token)
        except TokenError:
            if refresh_token:
                # اگر access_token منقضی شده، تلاش برای رفرش آن
                refresh_data = {'refresh': refresh_token}
                try:
                    refresh_response = requests.post(f'{settings.BACKEND_URL}/api/token/refresh/', data=refresh_data)
                except requests.RequestException as e:

                    return JsonResponse({"status": "failed", "message": "خطا در ارتباط با سرور."}, status=500)

                if refresh_response.status_code == 200:
                    # توکن جدید دریافت شد
                    new_access_token = refresh_response.json().get('access')
                    response = JsonResponse({
                        "status": "success",
                        "message": "توکن با موفقیت رفرش شد",
                        "user": str(user)
                    })
                    # دریافت CSRF token
                    csrf_token = get_token(request)

                    # محیط توسعه
                    # response.set_cookie('accessToken', new_access_token, httponly=True, secure=False, samesite='Lax')
                    # response.set_cookie('refreshToken', refresh_token, httponly=False, secure=False, samesite='Lax')
                    # response.set_cookie('csrftoken', csrf_token, httponly=False, secure=False, samesite='Lax')

                    # محیط پروداکشن
                    response.set_cookie('accessToken', new_access_token, httponly=True, secure=False, samesite='Lax')
                    response.set_cookie('refreshToken', refresh_token, httponly=False, secure=False, samesite='Lax')
                    response.set_cookie('csrftoken', csrf_token, httponly=False, secure=False, samesite='Lax')

                    return response
                else:
                    # رفرش توکن ناموفق بود
                    status_error = "رفرش توکن ناموفق بود"
                    return JsonResponse({"status": status_error, "message": "رفرش توکن ناموفق بود."}, status=401)
            else:
                # اگر توکن رفرش وجود ندارد

                status_error = "توکن رفرش وجود ندارد"
                return JsonResponse({"status": status_error, "message": "رفرش توکن وجود ندارد."}, status=407)

        # اگر access_token معتبر است
        status_error = "access_token معتبر است"
        return Response({"status": status_error, "message": "توکن معتبر است.", "user": str(user)})


class GetInfo(APIView):
    authentication_classes = [CookieJWTAuthentication]  # استفاده از کلاس احراز هویت جدید
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            # پس از احراز هویت موفق، کاربر به عنوان request.user در دسترس است
            user = request.user

            # استفاده از سریالایزر برای فرمت کردن داده‌ها
            serializer = MyUserSerializer(user)

            # ارسال اطلاعات کاربر
            return JsonResponse({'status': 'ok', 'user': serializer.data})

        except AuthenticationFailed as e:
            # در صورت بروز مشکل در احراز هویت
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=401)

        except MyUser.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'User not found!'}, status=404)



class SetImageUser(APIView):
    authentication_classes = [CookieJWTAuthentication]  # احراز هویت با JWT در کوکی
    permission_classes = [IsAuthenticated]  # تنها کاربران احراز هویت‌شده می‌توانند به این endpoint دسترسی داشته باشند
    parser_classes = (MultiPartParser, FormParser)  # اجازه می‌دهد فایل‌های چندقسمتی را دریافت کند

    def post(self, request):
        user = request.user  # کاربر احراز هویت‌شده

        if 'image' not in request.data:
            return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

        image = request.data['image']  # دریافت تصویر

        # در اینجا می‌توانید بررسی‌های اضافی انجام دهید (نوع فایل، اندازه، و غیره)

        # ذخیره تصویر در مدل کاربر
        user.image = image
        user.save()

        return Response({"message": "Image uploaded successfully!"}, status=status.HTTP_200_OK)


def logoutV1(request):
    print("request============================logout")
    print(request)
    print("request============================logout")

    # خروج کاربر از سامانه
    logout(request)

    # ایجاد response با موفقیت و تعیین وضعیت
    response = JsonResponse({"message": "شما از سامانه خارج شدید"}, status=200)

    # حذف کوکی‌های توکن
    response.delete_cookie('accessToken')
    response.delete_cookie('access_token')
    response.delete_cookie('refreshToken')
    response.delete_cookie('refresh_token')

    return response



class FollowAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        # اضافه کردن بررسی وجود کلید 'user_id'
        user_id = body.get('user_id')
        if user_id is None:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)



        user_to_follow = get_object_or_404(MyUser, id=user_id)
        request.user.follow(user_to_follow)
        return Response({"status": "success", "message": f"Following {user_to_follow.username}"}, status=status.HTTP_201_CREATED)



class UnFollowAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        # اضافه کردن بررسی وجود کلید 'user_id'
        user_id = body.get('user_id')
        if not user_id:
            return Response({"error": "User ID required"}, status=status.HTTP_400_BAD_REQUEST)

        user_to_unfollow = get_object_or_404(MyUser, id=user_id)
        request.user.unfollow(user_to_unfollow)
        return Response({"status": "success", "message": f"Unfollowed {user_to_unfollow.username}"}, status=status.HTTP_204_NO_CONTENT)



class IsFollowAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.is_anonymous:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        print("Checking if user is following...", user_id)
        user_to_check = get_object_or_404(MyUser, id=user_id)
        is_following = Follow.objects.filter(follower=request.user, followed=user_to_check).exists()
        return Response({"isFollowing": is_following}, status=status.HTTP_200_OK)



class UserDetailsFollowingAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # بررسی اینکه کاربر وارد شده است یا خیر
        if request.user.is_anonymous:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # یافتن کاربر بر اساس user_id
        user = get_object_or_404(MyUser, pk=user_id)

        # بدست آوردن تعداد فالوورها و دنبال‌شده‌ها

        followers_count = user.followers.count()  # اصلاح
        following_count = user.following.count()  # اصلاح

        # بررسی اینکه آیا کاربر درخواست‌دهنده (request.user) این کاربر را فالو کرده است یا خیر
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

        # بازگشت اطلاعات به سمت کلاینت
        data = {
            'followers': followers_count,  # تعداد فالوورها
            'following': following_count,  # تعداد دنبال‌شده‌ها
            'isFollowing': is_following,   # آیا کاربر درخواست‌دهنده این کاربر را فالو کرده است یا خیر
        }

        return Response(data, status=status.HTTP_200_OK)




class AddressListCreateView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        print("add address to list ....")
        print(serializer)
        print("add address to list ....")
        if serializer.is_valid():
            serializer.save(user=request.user)  # کاربر را به آدرس اضافه می‌کند
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # چاپ خطاهای اعتبارسنجی
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AddressDetailView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk, user=self.request.user)  # فقط آدرس‌های متعلق به کاربر فعلی را برمی‌گرداند
        except Address.DoesNotExist:
            return None

    def get(self, request, pk):
        address = self.get_object(pk)
        if address is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = self.get_object(pk)
        if address is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(pk)
        if address is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckTokenMobile(APIView):
    permission_classes = [IsAuthenticated]  # برای اطمینان از احراز هویت اولیه

    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')
        refresh_token = request.data.get('refresh_token')

        # مرحله 1: چک کردن معتبر بودن access_token
        try:
            # اگر access_token معتبر باشد، ادامه می‌دهد
            token = AccessToken(access_token)
            return Response({
                "status": "ok",
                "message": "Access token is valid",
                "access_token": str(token)  # توکن فعلی برمی‌گردد
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            # اگر access_token نامعتبر یا منقضی شده باشد
            if isinstance(e, InvalidToken):
                # مرحله 2: اگر access_token منقضی شده، بررسی refresh_token
                try:
                    refresh = RefreshToken(refresh_token)

                    # ایجاد توکن‌های جدید
                    new_access_token = str(refresh.access_token)
                    new_refresh_token = str(refresh)

                    # بازگشت توکن‌های جدید
                    return Response({
                        "status": "ok",
                        "message": "Access token refreshed",
                        "access_token": new_access_token,
                        "refresh_token": new_refresh_token
                    }, status=status.HTTP_200_OK)

                except TokenError:
                    # اگر refresh_token هم نامعتبر باشد، کاربر باید دوباره لاگین کند
                    return Response({
                        "status": "error",
                        "message": "Refresh token is invalid or expired. Please log in again."
                    }, status=status.HTTP_401_UNAUTHORIZED)

        # برای هر خطای ناشناخته دیگر
        return Response({
            "status": "error",
            "message": "Invalid request."
        }, status=status.HTTP_400_BAD_REQUEST)