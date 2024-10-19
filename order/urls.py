from django.urls import path, re_path

from catalogue.views import product_list, category_products, brand_products
from order.views import VerifyView, VerifyViewWeb, PaymentApiV1, PaymentVerifyApiV1

urlpatterns = [
    path('verify/', VerifyView.as_view(), name='verify-view'),
    path('verify/web/', VerifyViewWeb.as_view(), name='verify-view-web'),

    path('v1/payment/api/', PaymentApiV1.as_view(), name='payment-rebo-api-v1'),
    path('v1/payment/verify/', PaymentVerifyApiV1.as_view(), name='payment-rebo-verify-api-v1'),

]
