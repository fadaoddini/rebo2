from django.urls import path

from shop.views import SingleWeb, CartWeb, location_add, location_add_to_cart, delete_location, AllShopApi, MyShopApi, \
    AllProductsShopsApi, AddShopApi, CheckUserShopApi, AddProductApi, CategoryListApi, PackageListApi, \
    ChildCategoryListApi, InactiveProductsListView, ActiveProductsListView, FeaturedProductsListView, EditProductApi

urlpatterns = [
    path('single/<int:pk>/', SingleWeb.as_view(), name='shop-single-web'),
    path('cart/<int:pk>/', CartWeb.as_view(), name='shop-cart-web'),
    path('add_location/', location_add, name='location-add-web'),
    path('delete_location/<int:code_posti>/', delete_location, name='delete_location'),
    path('add_location/<int:location_id>/', location_add_to_cart, name='location-add-web-to-cart'),

    path('all_shop', AllShopApi.as_view(), name='all-shop-api'),
    path('add_shop', AddShopApi.as_view(), name='add-shop-api'),

    path('check_shop', CheckUserShopApi.as_view(), name='check-shop-api'),
    path('add-product/', AddProductApi.as_view(), name='add-product-api'),
    path('edit_product_shop/<int:product_id>/', EditProductApi.as_view(), name='edit-product-shop-api'),
    path('categories/', CategoryListApi.as_view(), name='category-list-api'),
    path('categories/children/<int:parent_id>/', ChildCategoryListApi.as_view(), name='child-category-list-api'),

    path('packages/', PackageListApi.as_view(), name='package-list-api'),

    path('products/inactive/', InactiveProductsListView.as_view(), name='inactive-products'),
    path('products/active/', ActiveProductsListView.as_view(), name='active-products'),
    path('products/featured/', FeaturedProductsListView.as_view(), name='featured-products'),

    path('my_shop', MyShopApi.as_view(), name='my-shop-api'),
    path('all_products_in_all_shops', AllProductsShopsApi.as_view(), name='all-products-shops-api'),

]
