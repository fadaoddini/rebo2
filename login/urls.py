from django.urls import path, re_path

from catalogue.views import product_list, category_products, brand_products
from login.views import register_user, verify_otp, SendOtp, VerifyCode, logouti

urlpatterns = [
    path('', register_user, name='login-mobile'),
    path('verify/', verify_otp, name='verify-otp'),
    path('logout/', logouti, name='logout'),
    path('sendOtp', SendOtp.as_view(), name='send-otp'),
    path('verifyCode', VerifyCode.as_view(), name='verify'),
]
