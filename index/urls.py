from django.urls import path, re_path

from catalogue.views import product_list, category_products, brand_products
from index.views import Profile, MainIndex, MainAdmin, MainIndexSearch, update_info, update_info_image, update_user, \
    ProfileWallet, ProfileEtc, ProfileProduct, ProfileLearn, MainProduct, MainRequest, ProfileRequest, \
    ProfileRequestMain, Api, SettingsApi
from info.views import add_farmer

urlpatterns = [
    # path('', MainAdmin.as_view(), name='index'),
    # path('admin/admin/', MainIndex.as_view(), name='administrator'),
    path('', MainIndex.as_view(), name='index'),
    path('api/', Api.as_view(), name='api'),
    path('search/', MainIndexSearch.as_view(), name='index-search'),
    path('admin/admin/', MainAdmin.as_view(), name='administrator'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/etc/', ProfileEtc.as_view(), name='profile-etc'),
    path('profile/product/', ProfileProduct.as_view(), name='profile-product'),
    path('profile/request/', ProfileRequest.as_view(), name='profile-request'),
    path('profile/request/main/', ProfileRequestMain.as_view(), name='profile-request-main'),
    path('profile/learn/', ProfileLearn.as_view(), name='profile-learn'),
    path('profile/wallet/', ProfileWallet.as_view(), name='profile-wallet'),
    path('profile/main/', MainProduct.as_view(), name='main-product'),
    path('profile/request/', MainRequest.as_view(), name='main-request'),
    path('update/profile/', update_info, name='update-info-profile'),
    path('update/profile/user/', update_user, name='update-user'),
    path('update/profile/image/', update_info_image, name='update-info-profile-image'),
    path('farmer/add/', add_farmer, name='add-farmer'),
    path('settings/', SettingsApi.as_view(), name='setting-api'),

]
