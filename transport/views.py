import json
import math
from django.utils import timezone
from django.contrib.auth import get_user_model as user_model
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from transport.forms import TransportForm, TransportReqForm
from transport.models import Transport, TransportReq, TransportType, Location, RouteMetrics, PriceList
from transport.serializers import TransportSerializer, TransportReqSerializer, TransportTypeSerializer, \
    LocationSerializer


class CreateTransportApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user  # استخراج کاربر از توکن JWT

        print("User from request:", user)  # برای دیباگ
        print("Files in request:", request.FILES)

        # استفاده از FormData در Django
        form = TransportForm(request.data, files=request.FILES)

        if form.is_valid():
            transport = form.save(commit=False)  # دریافت شیء مدل بدون ذخیره آن
            transport.user = user  # اختصاص کاربر به شیء مدل
            transport.save()  # ذخیره فرم با کاربر اختصاص داده شده
            return Response({"message": "Transport created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            print("Form validation errors:", form.errors)  # برای دیباگ
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTransportReqApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user  # استخراج کاربر از توکن JWT

        print("User from request:", user)  # برای دیباگ

        # استفاده از FormData در Django
        form = TransportReqForm(request.data)

        if form.is_valid():
            form.save()
            return Response({"message": "Transport Req created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            print("Form validation errors:", form.errors)  # برای دیباگ
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class AllTransportApi(APIView):
    def get(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 12  # تعداد اقلام در هر صفحه

        transports = Transport.objects.filter(status=True).all()
        result_page = paginator.paginate_queryset(transports, request)
        serializer = TransportSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class AllTypeTransportApi(APIView):
    def get(self, request, *args, **kwargs):
        types = TransportType.objects.all()
        serializer = TransportTypeSerializer(types, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class MyTransportApi(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        mobile = body['mobile']
        my_user = user_model()
        user = my_user.objects.filter(mobile=mobile).first()
        transport = Transport.objects.filter(user=user).all()
        serializer = TransportSerializer(transport, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class AllReqTransportByMobileApi(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        mobile = body['mobile']
        my_user = user_model()
        user = my_user.objects.filter(mobile=mobile).first()
        transport = Transport.objects.filter(user=user).first()

        all_my_req = transport.transportreqs.all()
        serializer = TransportReqSerializer(all_my_req, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class AllReqTransportByTypeApi(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        type_id = body.get('id')

        if not type_id:
            return Response({"error": "Type ID is required"}, status=400)

        # Step 1: Find the TransportType by ID
        try:
            transport_type = TransportType.objects.get(pk=type_id)
        except TransportType.DoesNotExist:
            return Response({"error": "TransportType not found"}, status=404)

        # Step 2: Find all Transport objects associated with this TransportType
        transports = Transport.objects.filter(transport_type=transport_type, status=True)

        # Step 3: Find all TransportReq objects related to these Transports
        transport_req_ids = transports.values_list('id', flat=True)
        all_req = TransportReq.objects.filter(my_transport__in=transport_req_ids, status=True)

        paginator = PageNumberPagination()
        paginator.page_size = 12  # تعداد اقلام در هر صفحه
        result_page = paginator.paginate_queryset(all_req, request)
        serializer = TransportReqSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)


class AllReqTransportApi(APIView):
    def get(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 16  # تعداد اقلام در هر صفحه
        # دریافت تاریخ و زمان فعلی
        now = timezone.now()
        all_my_req = TransportReq.objects.filter(status=True, expire_time__gt=now).all()
        result_page = paginator.paginate_queryset(all_my_req, request)
        serializer = TransportReqSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class AllLocationsApi(APIView):
    # استفاده از JWT برای احراز هویت
    authentication_classes = [JWTAuthentication]
    # تنها کاربران احراز هویت شده می‌توانند به این API دسترسی داشته باشند
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # لاگ کردن درخواست دریافتی برای بررسی
        print("Received GET request for all locations")

        # دریافت تمام مکان‌ها از پایگاه داده
        all_location = Location.objects.all()
        print(f"Found locations: {all_location}")

        # سریالایز کردن داده‌ها برای تبدیل به فرمت JSON
        serializer = LocationSerializer(all_location, many=True)
        print(f"Serialized data: {serializer.data}")

        # ارسال داده‌ها به کلاینت
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class CalculateRouteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        origin_id = request.data.get('origin_id')
        destination_id = request.data.get('destination_id')
        capacity = request.data.get('capacity')  # ظرفیت به کیلوگرم

        print(f"Received request with origin_id: {origin_id}, destination_id: {destination_id}, capacity: {capacity}")

        try:
            origin = Location.objects.get(id=origin_id)
            destination = Location.objects.get(id=destination_id)
            print(f"Found origin: {origin}, destination: {destination}")
        except Location.DoesNotExist:
            print("Error: Location not found")
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        # تلاش برای یافتن مسیرهای موجود بین مبدا و مقصد
        route = RouteMetrics.objects.filter(
            origin=origin,
            destination=destination
        ).first()

        # استخراج اطلاعات قیمت‌ها از PriceList
        try:
            price_list = PriceList.objects.latest('create_time')  # آخرین لیست قیمت
        except PriceList.DoesNotExist:
            return Response({'error': 'Price list not found'}, status=status.HTTP_404_NOT_FOUND)

        # محاسبه مسافت و به‌روزرسانی یا ایجاد مسیر
        if route:
            # اگر مسیر موجود است، فقط اطلاعات را به‌روزرسانی می‌کنیم
            print("RouteMetrics found, updating the route.")
            distance_km = route.distance_km  # استفاده از مسافت قبلی (در صورت نیاز به تغییر، می‌توان محاسبه کرد)
        else:
            # اگر مسیر موجود نیست، یک مسیر جدید ایجاد می‌کنیم
            print("RouteMetrics not found, creating a new route.")
            distance_km = calculate_distance(origin.latitude, origin.longitude, destination.latitude, destination.longitude)
            route = RouteMetrics(
                origin=origin,
                destination=destination,
                distance_km=distance_km
            )
            print(f"Created new route: {route}")

        # محاسبه هزینه‌ها بر اساس مسافت و ظرفیت (تن و کیلومتر)
        if capacity:
            min_cost = round((price_list.min_cost_per_one_ton * capacity) +
                             (price_list.min_cost_per_one_km * distance_km))
            max_cost = round((price_list.max_cost_per_one_ton * capacity) +
                             (price_list.max_cost_per_one_km * distance_km))
        else:
            min_cost = round(price_list.min_cost_per_one_km * distance_km)
            max_cost = round(price_list.max_cost_per_one_km * distance_km)

        # به‌روزرسانی اطلاعات مسیر با استفاده از هزینه‌های جدید
        route.min_cost = min_cost
        route.max_cost = max_cost
        route.save()

        response = {
            'distance_km': distance_km,
            'min_cost': min_cost,
            'max_cost': max_cost
        }
        print(f"Calculated and updated route: {response}")

        return Response(response, status=status.HTTP_200_OK)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def calculate_distance(lat1, lon1, lat2, lon2):
    return haversine(lat1, lon1, lat2, lon2)


def calculate_duration(distance):
    return distance / 100  # Example: 1 hour for every 100 km


def calculate_cost(distance):
    return distance * 0.5  # Example: 0.5 currency units per km
