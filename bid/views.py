import json

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication  # مطمئن شوید که این پکیج را نصب کرده‌اید

from login.models import MyUser
from order.models import Payment, Gateway
from order.utils import zpal_request_handler
from rebo import settings
from .models import Bid, Product
from rest_framework import status
from .serializers import BidSerializer


class BidView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        price = request.data.get('price')
        product_id = request.data.get('product_id')

        if not product_id or not price:
            return Response({'error': 'Price and product_id are required'}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        with transaction.atomic():
            bid, created = Bid.objects.update_or_create(
                user=user,
                product=product,
                defaults={'price': price, 'result': False}
            )
            try:
                myUser = MyUser.objects.get(pk=user.id)
                myUser.num_bid = myUser.num_bid - 1
                if myUser.num_bid == 0:
                    myUser.bider = False
                myUser.save()
            except MyUser.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "کاربر یافت نشد."
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Bid created/updated'})


class BidByProductTypeApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        # فیلتر کردن Bidها بر اساس نوع محصول
        bids = Bid.objects.filter(product__product_type=pk)

        # فیلتر و سورت کردن Bids با sell_buy = 1 (خریدار) و گرفتن 5 مورد از بیشترین قیمت‌ها
        buy_bids = bids.filter(product__sell_buy=1).order_by('-price')[:5]

        # فیلتر و سورت کردن Bids با sell_buy = 2 (فروشنده) و گرفتن 5 مورد از کمترین قیمت‌ها
        sell_bids = bids.filter(product__sell_buy=2).order_by('price')[:5]

        # ترکیب دو QuerySet
        combined_bids = list(buy_bids) + list(sell_bids)

        # سریالایز کردن داده‌های Bid
        serializer = BidSerializer(combined_bids, many=True)

        # برگرداندن داده‌ها به صورت پاسخ JSON
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print("Received price:", body.get('price'))
            print("Received num_bids:", body.get('num_bids'))  # دریافت تعداد بیدها
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=400)

        user = request.user
        price = body.get('price')
        num_bids = body.get('num_bids', 0)  # پیش‌فرض تعداد بیدها 0 است

        amount = price  # فرض می‌کنیم که مقدار پرداخت همان قیمت محصول است
        mobile = user.mobile  # فرض می‌کنیم که شماره موبایل کاربر در مدل User ذخیره شده است

        payment_link, authority = zpal_request_handler(
            settings.ZARRINPAL['merchant_id'],
            amount,
            "درخواست پیشنهاد",
            None,
            mobile,
            f"{settings.ADDRESS_SERVER}/payment/bid/verify/"  # استفاده از ADDRESS_SERVER
        )

        if payment_link:
            # ایجاد یک رکورد پرداخت در دیتابیس
            Payment.create_payment(authority, amount, user, product=None, num_bids=num_bids)  # اضافه کردن num_bids به متد create_payment

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
        user = request.user
        authority = request.query_params.get('authority')
        payment_status = request.query_params.get('status')  # وضعیت پرداخت از زارین‌پال

        # بررسی وجود payment
        payment = Payment.objects.filter(authority=authority).first()
        if not payment:
            return Response({
                "status": "error",
                "message": "پرداخت یافت نشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        gateway = Gateway.objects.filter(gateway_code="zarrinpal").first()
        if gateway is None:
            return Response({
                "status": "error",
                "message": "درگاه پرداخت فعال یافت نشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        verified = payment.verify({
            'authority': authority,
            'status': payment_status
        })

        if verified and payment_status == "OK":
            with transaction.atomic():
                if payment.num_bids > 0:
                    try:
                        myUser = MyUser.objects.get(pk=user.id)
                        myUser.bider = True
                        myUser.num_bid += payment.num_bids
                        myUser.save()
                    except MyUser.DoesNotExist:
                        return Response({
                            "status": "error",
                            "message": "کاربر یافت نشد."
                        }, status=status.HTTP_400_BAD_REQUEST)

                payment.is_paid = True
                payment.save()

            return Response({
                "status": "success",
                "message": "پرداخت با موفقیت انجام شد."
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "پرداخت ناموفق بود."
        }, status=status.HTTP_400_BAD_REQUEST)


class CheckBidApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        num_bid = user.num_bid  # تعداد پیشنهادهای مجاز برای کاربر

        if user.bider and num_bid > 0:
            return Response({
                "status": "success",
                "num_bid": num_bid,  # ارسال تعداد پیشنهادهای مجاز به فرانت‌اند
                "message": "شما می توانید پیشنهاد ثبت کنید"
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "متاسفانه شما نمی توانید پیشنهادی ثبت کنید"
        }, status=status.HTTP_400_BAD_REQUEST)