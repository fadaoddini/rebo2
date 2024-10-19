from django.urls import path

from transport.views import AllTransportApi, MyTransportApi, AllReqTransportApi, AllReqTransportByMobileApi, \
    AllTypeTransportApi, AllReqTransportByTypeApi, CreateTransportApi, CreateTransportReqApi, CalculateRouteView, \
    AllLocationsApi, NotPayTransportReqApi, NotActiveTransportReqApi, ActiveTransportReqApi, \
    PaymentVerifyApi, PaymentApi, ApiTransportReqDelete, CreateTransportApiV1, AllTypeTransportApiV1, AllTransportApiV1, \
    NotPayTransportReqApiV1, NotActiveTransportReqApiV1, ActiveTransportReqApiV1, MyTransportApiV1, \
    ApiTransportReqDeleteV1, PaymentApiV1, PaymentVerifyApiV1, AllLocationsApiV1, CalculateRouteViewV1, \
    CreateTransportReqApiV1, AllReqTransportByTypeApiV1, AllReqTransportApiV1

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

    path('v1/create_transport', CreateTransportApiV1.as_view(), name='create-transport-api-v1'),
    path('v1/all_type_transport', AllTypeTransportApiV1.as_view(), name='all-type_transport-api-v1'),
    path('v1/all_transport', AllTransportApiV1.as_view(), name='all-transport-api-v1'),
    path('v1/not_pay_transport_req_api', NotPayTransportReqApiV1.as_view(), name='not-pay-transport-req-api-v1'),
    path('v1/not_active_transport_req_api', NotActiveTransportReqApiV1.as_view(), name='not-active-transport-req-api-v1'),
    path('v1/active_transport_req_api', ActiveTransportReqApiV1.as_view(), name='active-transport-req-api-v1'),
    path('v1/my_transport', MyTransportApiV1.as_view(), name='my-transport-api-v1'),
    path('v1/delete_transport_req_api/', ApiTransportReqDeleteV1.as_view(), name='delete-transport-req-api-v1'),
    path('v1/payment/api/', PaymentApiV1.as_view(), name='payment-transport-api-v1'),
    path('v1/payment/verify/', PaymentVerifyApiV1.as_view(), name='payment-transport-verify-api-v1'),
    path('v1/all_locations', AllLocationsApiV1.as_view(), name='all-locations-v1'),
    path('v1/calculate_route/', CalculateRouteViewV1.as_view(), name='calculate_route-v1'),
    path('v1/create_transport_req', CreateTransportReqApiV1.as_view(), name='create-transport-req-api-v1'),
    path('v1/delete_transport_req_api/', ApiTransportReqDeleteV1.as_view(), name='delete-transport-req-api-v1'),
    path('v1/all_req_transport_by_type', AllReqTransportByTypeApiV1.as_view(), name='all-req-transport-by-type-api-v1'),
    path('v1/all_req_transport', AllReqTransportApiV1.as_view(), name='all-req-transport-api-v1'),

]
