from django.urls import path, re_path

from catalogue.views import product_list, category_products, brand_products
from order.views import VerifyView, VerifyViewWeb

urlpatterns = [
    path('verify/', VerifyView.as_view(), name='verify-view'),
    path('verify/web/', VerifyViewWeb.as_view(), name='verify-view-web'),

]
