from django.urls import path

from shop.views import SingleWeb, CartWeb, location_add, location_add_to_cart, delete_location, AllShopApi, MyShopApi, \
    AllProductsShopsApi, AddShopApi, CheckUserShopApi, AddProductApi, CategoryListApi, PackageListApi, \
    ChildCategoryListApi, InactiveProductsListView, ActiveProductsListView, FeaturedProductsListView, EditProductApi, \
    AllShopApiV1, AddShopApiV1, CheckUserShopApiV1, AddProductApiV1, EditProductApiV1, CategoryListApiV1, \
    ChildCategoryListApiV1, PackageListApiV1, InactiveProductsListViewV1, ActiveProductsListViewV1, \
    FeaturedProductsListViewV1, MyShopApiV1, AllProductsShopsApiV1, ProductByIdApiV1, CartAPIView

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






    path('v1/all_shop', AllShopApiV1.as_view(), name='all-shop-api-v1'),
    path('v1/add_shop', AddShopApiV1.as_view(), name='add-shop-api-v1'),

    path('v1/check_shop', CheckUserShopApiV1.as_view(), name='check-shop-api-v1'),
    path('v1/add-product/', AddProductApiV1.as_view(), name='add-product-api-v1'),
    path('v1/edit_product_shop/<int:product_id>/', EditProductApiV1.as_view(), name='edit-product-shop-api-v1'),
    path('v1/categories/', CategoryListApiV1.as_view(), name='category-list-api'),
    path('v1/categories/children/<int:parent_id>/', ChildCategoryListApiV1.as_view(), name='child-category-list-api-v1'),

    path('v1/packages/', PackageListApiV1.as_view(), name='package-list-api-v1'),

    path('v1/products/inactive/', InactiveProductsListViewV1.as_view(), name='inactive-products-v1'),
    path('v1/products/active/', ActiveProductsListViewV1.as_view(), name='active-products-v1'),
    path('v1/products/featured/', FeaturedProductsListViewV1.as_view(), name='featured-products-v1'),

    path('v1/my_shop', MyShopApiV1.as_view(), name='my-shop-api-v1'),
    path('v1/all_products_in_all_shops', AllProductsShopsApiV1.as_view(), name='all-products-shops-api-v1'),
    path('v1/product_by_id/<int:id>/', ProductByIdApiV1.as_view(), name='product-by-id-v1'),

    path('v1/cart/', CartAPIView.as_view(), name='cart-api-v1'),  # برای نمایش سبد خرید و افزودن محصول
    path('v1/cart/<int:item_id>/', CartAPIView.as_view(), name='cart-item-api-v1'),  # برای حذف محصول از سبد خرید

]
