from django.conf import settings
from django.db import transaction
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from login.views import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from order.utils import zpal_request_handler
from order.models import Payment, Gateway
from order.utils import zpal_payment_checker
from transaction.models import Transaction


# Create your views here.

class VerifyView(View):
    template_name = 'ecommerce/web/verify_wallet.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')
        payment = Payment.objects.filter(authority=authority).first()

        if payment.is_paid:
            ref_id = "تراکنش قبلا ثبت شده است"
            is_paid = 0
            return render(request, template_name=self.template_name, context={'is_paid': is_paid, 'ref_id': ref_id},
                          content_type=None, status=None, using=None)
        else:
            amount = payment.amount
            is_paid, ref_id = zpal_payment_checker(settings.ZARRINPAL['merchant_id'], amount, authority)
            if status == "OK":
                if payment:
                    payment.is_paid = True
                    with transaction.atomic():
                        payment.save()
                        amount = amount * 10
                        Transaction.sharj(user, amount, 1)
            else:
                print("NOOOOOO")
            return render(request, template_name=self.template_name, context={'is_paid': is_paid, 'ref_id': ref_id},
                          content_type=None, status=None, using=None)


class VerifyViewWeb(View):
    template_name = 'ecommerce/verify_wallet.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        authority = request.GET.get('Authority')
        amount = request.GET.get('amount')
        status = request.GET.get('status')
        payment = Payment.objects.filter(authority=authority).first()
        is_paid, ref_id = zpal_payment_checker(settings.ZARRINPAL['merchant_id'], amount, authority)
        if status == "OK":
            print("====================transactions=============================")
            if payment:
                payment.is_paid = False
                print("no")
                print("====================transactions=============================")

            else:
                payment.is_paid = True
                with transaction.atomic():
                    payment.save()
                    amount = amount * 10
                    Transaction.sharj(user, amount, 1)

        else:
            print("NOOOOOO")
        return render(request, template_name=self.template_name, context={'is_paid': is_paid, 'ref_id': ref_id},
                      content_type=None, status=None, using=None)




class PaymentApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            body = request.data
        except Exception as e:
            return Response({"error": f"Error parsing request data: {str(e)}"}, status=400)


        user = request.user
        transport_req_id = body.get('transport_id')
        transport_req = TransportReq.objects.filter(id=transport_req_id).first()

        if not transport_req:
            return Response({"error": "Transport request not found."}, status=404)

        amount = 25000
        mobile = user.mobile

        payment_link, authority = zpal_request_handler(
            settings.ZARRINPAL['merchant_id'],
            amount,
            "درخواست ترانزیت",
            None,
            mobile,
            f"{settings.ADDRESS_SERVER}/payment/zarinpal"
        )

        if payment_link:
            Payment.create_payment(authority, amount, user, transport=transport_req)
            return Response({
                "status": "success",
                "payment_link": payment_link
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "خطا در ایجاد لینک پرداخت."
        }, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        authority = request.query_params.get('authority')
        payment_status = request.query_params.get('status')




        payment = Payment.objects.filter(authority=authority).first()

        if not payment:
            return Response({
                "status": "error",
                "message": "پرداخت یافت نشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        gateway = Gateway.objects.filter(gateway_code="zarrinpal").first()

        if not gateway:
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
                print("وارد اتمیک شدیم")
                if payment.transport:
                    print("پرداخت موفقیت امیز بود")
                    transport = TransportReq.objects.filter(pk=payment.transport.pk).first()
                    print("info is :", transport)
                    if transport:
                        transport.is_successful = True
                        transport.expire_time = timezone.now() + timedelta(hours=24)
                        transport.save()
                    print("درخواست اوکی شد")
                payment.is_paid = True
                print("درخواست پرداخت شد")
                payment.save()
            print("پرداخت ذخیره شد")
            return Response({
                "status": "success",
                "message": "پرداخت با موفقیت انجام شد."
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "پرداخت ناموفق بود."
        }, status=status.HTTP_400_BAD_REQUEST)