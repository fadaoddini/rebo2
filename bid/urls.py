from django.urls import path

from bid.views import BidView, BidByProductTypeApi, PaymentApi, PaymentVerifyApi, CheckBidApi

urlpatterns = [

    path('add_bid_api/', BidView.as_view(), name='add-bid-api'),
    path('bid_by_type/api/<int:pk>/', BidByProductTypeApi.as_view(), name='statistic-api'),

    path('payment/api/', PaymentApi.as_view(), name='payment-bid-api'),
    path('payment/verify/', PaymentVerifyApi.as_view(), name='payment-bid-verify-api'),
    path('check_bid/', CheckBidApi.as_view(), name='check-bid-api'),





    path('v1/add_bid_api/', BidView.as_view(), name='add-bid-api-v1'),

]
