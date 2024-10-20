from django.urls import path

from catalogue.views import product_list, ProductDetail, category_products, brand_products, add_product, add_request, \
    my_product_list, my_request_list, form_add_product, check_type_product_ajax, check_attr_product_ajax, \
    form_add_request, bazar_sell, bazar_buy, ProductApi, ProductSingleApi, create_chart_top, ProductWeb, AllProductWeb, \
    form_add_product_web, AllRequestWeb, form_add_request_web, \
    AllProductAndRequestWeb, form_add_bid_web, form_bid_ok, form_bid_no, bazar_sell_web, BazarWeb, \
    InBazarWeb, AddProduct, AddRequest, RequestDetail, TypesApi, ApiProductCreateAPIView, CategoryListAPIView, \
    ProductTypeListAPIView, ProductAttributeListAPIView, AttributeValueListAPIView, ProductByIdAPIView, InBazarApi, \
    BazarStatsApi, PaymentApi, PaymentVerifyApi, ProductNotPayMeAPIView, ProductNotActiveMeAPIView, \
    ProductActiveMeAPIView, ApiProductDeleteAPIView, BidSellListApi, BidBuyListApi, \
    SellBidSingleBazarApi, BuyBidSingleBazarApi, SellSingleBazarApi, BuySingleBazarApi, ApiProductCreateAPIViewV1, \
    TypeByIdApi, ChartByTypeIdApi, BidSellListByTypeApi, BidBuyListByTypeApi, BidSellListChartApi, BidBuyListChartApi, \
    CategoryNameApi, AllTypeApi

urlpatterns = [
    path('product/list/', product_list, name='product-list'),
    path('bazar/sell/<int:pk>/', bazar_sell, name='bazar-sell'),
    path('bazar/sell/web/<int:pk>/', bazar_sell_web, name='bazar-sell-web'),
    path('bazar/web/', BazarWeb.as_view(), name='bazar-web'),

    path('bazar/buy/', bazar_buy, name='bazar-buy'),
    path('chart1/', create_chart_top, name='create-chart-top'),
    path('add_product/<int:pk>/', add_product, name='add_product'),
    path('add_product/web/<int:pk>/', AddProduct.as_view(), name='add-product-web'),
    path('check_type_product_ajax/', check_type_product_ajax, name='check-type-product-ajax'),
    path('check_attr_product_ajax/', check_attr_product_ajax, name='check-attr-product-ajax'),
    path('send/add_product/', form_add_product, name='form-add-product'),
    path('send/add_product/web/', form_add_product_web, name='form-add-product-web'),
    path('send/add_bid/web/<int:upc>/', form_add_bid_web, name='form-add-bid-web'),
    path('bid/ok/<int:pk>/', form_bid_ok, name='form-bid-ok'),
    path('bid/no/<int:pk>/', form_bid_no, name='form-bid-no'),
    path('send/add_request/', form_add_request, name='form-add-request'),
    path('send/add_request/web/', form_add_request_web, name='form-add-request-web'),
    path('add_request/<int:pk>/', add_request, name='add_request'),
    path('add_request/web/<int:pk>/', AddRequest.as_view(), name='add-req-web-web'),
    path('my_product_list/<int:pk>/', my_product_list, name='my_product_list'),
    path('my_request_list/<int:pk>/', my_request_list, name='my_request_list'),
    path('product/detail/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('request/detail/<int:pk>/', RequestDetail.as_view(), name='request-detail'),
    path('category/<int:pk>/products/', category_products, name='category_products'),
    path('brand/<int:pk>/products/', brand_products, name='brand_products'),
    path('product/web/', ProductWeb.as_view(), name='product-web'),
    path('all/web/', AllProductAndRequestWeb.as_view(), name='all-all-web-web'),
    path('all/product/web/', AllProductWeb.as_view(), name='product-web-web'),
    path('all/request/web/', AllRequestWeb.as_view(), name='request-web-web'),
    path('sortby', ProductApi.as_view(), name='all-product-api'),
    path('single', ProductSingleApi.as_view(), name='single-product-api'),
    path('all_types', TypesApi.as_view(), name='statistic'),

    path('add_product_api/', ApiProductCreateAPIView.as_view(), name='add-product-api'),
    path('delete_product_api/', ApiProductDeleteAPIView.as_view(), name='delete-product-api'),
    path('categories_api/', CategoryListAPIView.as_view(), name='category-list-api'),
    path('product_by_id_api/', ProductByIdAPIView.as_view(), name='product-bu-id-api'),


    path('product_not_pay_me/', ProductNotPayMeAPIView.as_view(), name='product-not-pay-me-api'),
    path('product_not_active_me/', ProductNotActiveMeAPIView.as_view(), name='product-not-active-me-api'),
    path('product_active_me/', ProductActiveMeAPIView.as_view(), name='product-active-me-api'),


    path('product_types/', ProductTypeListAPIView.as_view(), name='product-type-list-api'),
    path('product_attributes/', ProductAttributeListAPIView.as_view(), name='product-attribute-list-api'),
    path('attribute_values/', AttributeValueListAPIView.as_view(), name='attribute-value-list-api'),

    path('bazar/web/<int:pk>/', InBazarWeb.as_view(), name='bazar-web-in'),
    path('bazar/api/<int:pk>/', InBazarApi.as_view(), name='bazar-api-in'),
    path('statistic/api/<int:pk>/', BazarStatsApi.as_view(), name='statistic-api'),


    path('payment/api/', PaymentApi.as_view(), name='payment-api'),
    path('payment/verify/', PaymentVerifyApi.as_view(), name='payment-verify-api'),




    path('v1/all_types', TypesApi.as_view(), name='statistic'),
    path('v1/all_type', AllTypeApi.as_view(), name='all-type'),



    path('v1/bazar/api/<int:pk>/', InBazarApi.as_view(), name='bazar-api-in'),
    path('v1/sell/single/<int:pk>/', SellSingleBazarApi.as_view(), name='sell-api-single'),
    path('v1/buy/single/<int:pk>/', BuySingleBazarApi.as_view(), name='buy-api-single'),
    path('v1/sell/bid/<int:pk>/', SellBidSingleBazarApi.as_view(), name='bid-sell-api-single'),
    path('v1/buy/bid/<int:pk>/', BuyBidSingleBazarApi.as_view(), name='bid-buy-api-single'),
    path('v1/sell/bid/list/<int:pk>/', BidSellListApi.as_view(), name='bid-sell-api-list'),
    path('v1/buy/bid/list/<int:pk>/', BidBuyListApi.as_view(), name='bid-buy-api-list'),
    path('v1/sell/bid/list/chart/<int:pk>/', BidSellListChartApi.as_view(), name='bid-sell-api-list-chart'),
    path('v1/buy/bid/list/chart/<int:pk>/', BidBuyListChartApi.as_view(), name='bid-buy-api-list-chart'),
    path('v1/category/name/<int:pk>/', CategoryNameApi.as_view(), name='name-cat'),
    path('v1/all_types', TypesApi.as_view(), name='all-types-v1'),
    path('v1/product_types/', ProductTypeListAPIView.as_view(), name='product-type-list-api-v1'),
    path('v1/product_attributes/', ProductAttributeListAPIView.as_view(), name='product-attribute-list-api-v1'),
    path('v1/attribute_values/', AttributeValueListAPIView.as_view(), name='attribute-value-list-api-v1'),
    path('v1/add_product_api/', ApiProductCreateAPIViewV1.as_view(), name='add-product-api-v1'),
    path('v1/type/<int:id>/', TypeByIdApi.as_view(), name='type-by-id-api-v1'),
    path('v1/chart/<int:id>/', ChartByTypeIdApi.as_view(), name='chart-api-v1'),
    path('v1/sell/bid/all/<int:pk>/', BidSellListByTypeApi.as_view(), name='bid-sell-api-all'),
    path('v1/buy/bid/all/<int:pk>/', BidBuyListByTypeApi.as_view(), name='bid-buy-api-all'),

]
