from django.urls import path

from transport.views import AllTransportApi, MyTransportApi, AllReqTransportApi, AllReqTransportByMobileApi, \
    AllTypeTransportApi, AllReqTransportByTypeApi, CreateTransportApi, CreateTransportReqApi, CalculateRouteView, \
    AllLocationsApi, NotPayTransportReqApi, NotActiveTransportReqApi, ActiveTransportReqApi, \
    PaymentVerifyApi, PaymentApi, ApiTransportReqDelete

urlpatterns = [
    path('all_transport', AllTransportApi.as_view(), name='all-transport-api'),
    path('all_type_transport', AllTypeTransportApi.as_view(), name='all-type_transport-api'),
    path('my_transport/', MyTransportApi.as_view(), name='my-transport-api'),
    path('all_req_transport_by_mobile', AllReqTransportByMobileApi.as_view(), name='all-req-transport-by-mobile-api'),

    path('not_pay_transport_req_api', NotPayTransportReqApi.as_view(), name='not-pay-transport-req-api'),
    path('not_active_transport_req_api', NotActiveTransportReqApi.as_view(), name='not-active-transport-req-api'),
    path('active_transport_req_api', ActiveTransportReqApi.as_view(), name='active-transport-req-api'),

    path('delete_transport_req_api/', ApiTransportReqDelete.as_view(), name='delete-transport-req-api'),

    path('all_req_transport_by_type', AllReqTransportByTypeApi.as_view(), name='all-req-transport-by-type-api'),
    path('all_req_transport', AllReqTransportApi.as_view(), name='all-req-transport-api'),
    path('create_transport', CreateTransportApi.as_view(), name='create-transport-api'),
    path('create_transport_req', CreateTransportReqApi.as_view(), name='create-transport-req-api'),
    path('calculate_route/', CalculateRouteView.as_view(), name='calculate_route'),
    path('all_locations', AllLocationsApi.as_view(), name='all-locations'),

    path('payment/api/', PaymentApi.as_view(), name='payment-transport-api'),
    path('payment/verify/', PaymentVerifyApi.as_view(), name='payment-transport-verify-api'),


]
