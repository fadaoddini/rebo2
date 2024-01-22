from django.urls import path, re_path

from catalogue.views import product_list, category_products, brand_products
from info.views import info, update_info

urlpatterns = [
    path('before/info/', info, name='info-before'),
    path('update/before/', update_info, name='update-info-before'),
]
