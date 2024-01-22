from django.conf import settings
from django.db import transaction
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from order.models import Payment
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

