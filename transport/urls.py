from django.urls import path

from transport.views import AllTransportApi, MyTransportApi, AllReqTransportApi, AllReqTransportByMobileApi, \
    AllTypeTransportApi, AllReqTransportByTypeApi, CreateTransportApi, CreateTransportReqApi, CalculateRouteView, \
    AllLocationsApi

urlpatterns = [
    path('all_transport', AllTransportApi.as_view(), name='all-transport-api'),
    path('all_type_transport', AllTypeTransportApi.as_view(), name='all-type_transport-api'),
    path('my_transport', MyTransportApi.as_view(), name='my-transport-api'),
    path('all_req_transport_by_mobile', AllReqTransportByMobileApi.as_view(), name='all-req-transport-by-mobile-api'),
    path('all_req_transport_by_type', AllReqTransportByTypeApi.as_view(), name='all-req-transport-by-type-api'),
    path('all_req_transport', AllReqTransportApi.as_view(), name='all-req-transport-api'),
    path('create_transport', CreateTransportApi.as_view(), name='create-transport-api'),
    path('create_transport_req', CreateTransportReqApi.as_view(), name='create-transport-req-api'),
    path('calculate_route/', CalculateRouteView.as_view(), name='calculate_route'),
    path('all_locations', AllLocationsApi.as_view(), name='all-locations'),
]
