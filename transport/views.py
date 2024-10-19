import json
import math
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model as user_model
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from login.models import MyUser
from login.views import CookieJWTAuthentication
from order.models import Payment, Gateway
from order.utils import zpal_request_handler
from rebo import settings
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



class CreateTransportApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
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

        transports = Transport.objects.filter(status=True).all()
        serializer = TransportSerializer(transports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllTypeTransportApi(APIView):
    def get(self, request, *args, **kwargs):
        types = TransportType.objects.all()
        serializer = TransportTypeSerializer(types, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class MyTransportApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print("==============***********************MyTransportApi******************======================")
        try:
            # کاربر از طریق request.user که توسط JWTAuthentication احراز هویت شده است
            user = request.user

            # استخراج اطلاعات حمل و نقل براساس کاربر
            transports = Transport.objects.filter(user=user)
            if not transports.exists():
                return Response({'message': 'No transports found for this user.'}, status=404)

            serializer = TransportSerializer(transports, many=True)
            return Response(serializer.data)

        except Transport.DoesNotExist:
            return Response({'error': 'Transport not found'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


class AllReqTransportByMobileApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        print("user========================AllReqTransportByMobileApi")
        print(user)
        mobile = user.mobile
        my_user = user_model()
        user = my_user.objects.filter(mobile=mobile).first()
        transport = Transport.objects.filter(user=user).first()

        all_my_req = transport.transportreqs.all()
        serializer = TransportReqSerializer(all_my_req, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class NotPayTransportReqApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # حذف استفاده غیرضروری از user_model و دسترسی مستقیم به request.user
        mobile = user.mobile
        my_user = user_model()
        # بهینه‌سازی پرس‌وجو
        user = get_object_or_404(my_user, mobile=mobile)
        transports = user.transports.select_related('transport_type').all()

        # بهینه‌سازی و حذف استفاده غیرضروری از all()
        all_my_not_pay = TransportReq.objects.filter(
            my_transport__in=transports, is_successful=False
        ).select_related('origin', 'destination', 'my_transport').all()

        # استفاده از serializer برای تبدیل داده‌ها
        serializer = TransportReqSerializer(all_my_not_pay, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NotActiveTransportReqApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # حذف استفاده غیرضروری از user_model و دسترسی مستقیم به request.user
        mobile = user.mobile
        my_user = user_model()
        user = get_object_or_404(my_user, mobile=mobile)

        # استفاده از select_related برای بهینه‌سازی پرس‌وجو
        transports = user.transports.select_related('transport_type').all()

        all_my_not_active = TransportReq.objects.filter(
            my_transport__in=transports, is_successful=True, status=False
        ).select_related('origin', 'destination', 'my_transport')

        # استفاده از serializer برای تبدیل داده‌ها
        serializer = TransportReqSerializer(all_my_not_active, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveTransportReqApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # حذف استفاده غیرضروری از user_model و دسترسی مستقیم به request.user
        mobile = user.mobile
        my_user = user_model()
        user = get_object_or_404(my_user, mobile=mobile)

        # استفاده از select_related برای بهینه‌سازی پرس‌وجو
        transports = user.transports.select_related('transport_type').all()

        all_my_active = TransportReq.objects.filter(
            my_transport__in=transports, is_successful=True, status=True
        ).select_related('origin', 'destination', 'my_transport')
        print("all_my_active")
        print(all_my_active)
        print("all_my_active")
        # استفاده از serializer برای تبدیل داده‌ها
        serializer = TransportReqSerializer(all_my_active, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiTransportReqDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        transport_req_id = request.data.get('transport_req_id')  # دریافت ID محصول از داده‌های درخواست
        if not transport_req_id:
            return Response({"status": "error", "message": "transport ID is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        transport_req = get_object_or_404(TransportReq, id=transport_req_id)

        # بررسی مالکیت ترانزیت
        if transport_req.my_transport.user != request.user:
            return Response({"status": "error", "message": "You do not have permission to delete this transport"},
                            status=status.HTTP_403_FORBIDDEN)

        transport_req.delete()

        return Response({"status": "success", "message": "transport deleted successfully!"},
                        status=status.HTTP_200_OK)


class PaymentApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            body = request.data
        except Exception as e:
            return Response({"error": f"Error parsing request data: {str(e)}"}, status=400)

        user = request.user
        transport_req_id = body.get('transport_id')
        transport_req = TransportReq.objects.filter(id=transport_req_id).first()

        if not transport_req:
            return Response({"error": "Transport request not found."}, status=404)

        amount = 450
        mobile = user.mobile

        payment_link, authority = zpal_request_handler(
            settings.ZARRINPAL['merchant_id'],
            amount,
            "درخواست ترانزیت",
            None,
            mobile,
            f"{settings.ADDRESS_SERVER}/payment/transport/verify/"
        )

        if payment_link:
            Payment.create_payment(authority, amount, user, transport=transport_req)
            return Response({
                "status": "success",
                "payment_link": payment_link
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "خطا در ایجاد لینک پرداخت."
        }, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        authority = request.query_params.get('authority')
        payment_status = request.query_params.get('status')

        payment = Payment.objects.filter(authority=authority).first()
        if not payment:
            return Response({
                "status": "error",
                "message": "پرداخت یافت نشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        gateway = Gateway.objects.filter(gateway_code="zarrinpal").first()
        if not gateway:
            return Response({
                "status": "error",
                "message": "درگاه پرداخت فعال یافت نشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        verified = payment.verify({
            'authority': authority,
            'status': payment_status
        })

        if verified and payment_status == "OK":
            with transaction.atomic():
                if payment.transport:
                    transport = TransportReq.objects.filter(pk=payment.transport.pk).first()
                    if transport:
                        transport.is_successful = True
                        transport.expire_time = timezone.now() + timedelta(hours=24)
                        transport.save()
                payment.is_paid = True
                payment.save()

            return Response({
                "status": "success",
                "message": "پرداخت با موفقیت انجام شد."
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "پرداخت ناموفق بود."
        }, status=status.HTTP_400_BAD_REQUEST)


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
        all_my_req = TransportReq.objects.filter(status=True, expire_time__gt=now, is_successful=True).order_by(
            'id').all()
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
            distance_km = calculate_distance(origin.latitude, origin.longitude, destination.latitude,
                                             destination.longitude)
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



class AllTypeTransportApiV1(APIView):
    def get(self, request, *args, **kwargs):
        types = TransportType.objects.all()
        serializer = TransportTypeSerializer(types, many=True)
        print("====================================AllTypeTransportApiV1=====================================")
        print(serializer.data)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class AllTransportApiV1(APIView):
    def get(self, request, *args, **kwargs):

        transports = Transport.objects.filter(status=True).all()
        serializer = TransportSerializer(transports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class NotPayTransportReqApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # حذف استفاده غیرضروری از user_model و دسترسی مستقیم به request.user
        mobile = user.mobile
        my_user = user_model()
        # بهینه‌سازی پرس‌وجو
        user = get_object_or_404(my_user, mobile=mobile)
        transports = user.transports.select_related('transport_type').all()

        # بهینه‌سازی و حذف استفاده غیرضروری از all()
        all_my_not_pay = TransportReq.objects.filter(
            my_transport__in=transports, is_successful=False
        ).select_related('origin', 'destination', 'my_transport').all()

        # استفاده از serializer برای تبدیل داده‌ها
        serializer = TransportReqSerializer(all_my_not_pay, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NotActiveTransportReqApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # حذف استفاده غیرضروری از user_model و دسترسی مستقیم به request.user
        mobile = user.mobile
        my_user = user_model()
        user = get_object_or_404(my_user, mobile=mobile)

        # استفاده از select_related برای بهینه‌سازی پرس‌وجو
        transports = user.transports.select_related('transport_type').all()

        all_my_not_active = TransportReq.objects.filter(
            my_transport__in=transports, is_successful=True, status=False
        ).select_related('origin', 'destination', 'my_transport')

        # استفاده از serializer برای تبدیل داده‌ها
        serializer = TransportReqSerializer(all_my_not_active, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveTransportReqApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # حذف استفاده غیرضروری از user_model و دسترسی مستقیم به request.user
        mobile = user.mobile
        my_user = user_model()
        user = get_object_or_404(my_user, mobile=mobile)

        # استفاده از select_related برای بهینه‌سازی پرس‌وجو
        transports = user.transports.select_related('transport_type').all()

        all_my_active = TransportReq.objects.filter(
            my_transport__in=transports, is_successful=True, status=True
        ).select_related('origin', 'destination', 'my_transport')
        print("all_my_active")
        print(all_my_active)
        print("all_my_active")
        # استفاده از serializer برای تبدیل داده‌ها
        serializer = TransportReqSerializer(all_my_active, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class MyTransportApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print("==============***********************MyTransportApi******************======================")
        try:
            # کاربر از طریق request.user که توسط JWTAuthentication احراز هویت شده است
            user = request.user

            # استخراج اطلاعات حمل و نقل براساس کاربر
            transports = Transport.objects.filter(user=user)
            if not transports.exists():
                return Response({'message': 'No transports found for this user.'}, status=404)

            serializer = TransportSerializer(transports, many=True)
            return Response(serializer.data)

        except Transport.DoesNotExist:
            return Response({'error': 'Transport not found'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)



class ApiTransportReqDeleteV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        transport_req_id = request.data.get('transport_req_id')  # دریافت ID محصول از داده‌های درخواست
        if not transport_req_id:
            return Response({"status": "error", "message": "transport ID is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        transport_req = get_object_or_404(TransportReq, id=transport_req_id)

        # بررسی مالکیت ترانزیت
        if transport_req.my_transport.user != request.user:
            return Response({"status": "error", "message": "You do not have permission to delete this transport"},
                            status=status.HTTP_403_FORBIDDEN)

        transport_req.delete()

        return Response({"status": "success", "message": "transport deleted successfully!"},
                        status=status.HTTP_200_OK)



class PaymentApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            body = request.data
        except Exception as e:
            return Response({"error": f"Error parsing request data: {str(e)}"}, status=400)


        user = request.user
        transport_req_id = body.get('transport_id')
        transport_req = TransportReq.objects.filter(id=transport_req_id).first()

        if not transport_req:
            return Response({"error": "Transport request not found."}, status=404)

        amount = 25000
        mobile = user.mobile

        payment_link, authority = zpal_request_handler(
            settings.ZARRINPAL['merchant_id'],
            amount,
            "درخواست ترانزیت",
            None,
            mobile,
            f"{settings.ADDRESS_SERVER}/payment/zarinpal"
        )

        if payment_link:
            Payment.create_payment(authority, amount, user, transport=transport_req)
            return Response({
                "status": "success",
                "payment_link": payment_link
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "خطا در ایجاد لینک پرداخت."
        }, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        authority = request.query_params.get('authority')
        payment_status = request.query_params.get('status')




        payment = Payment.objects.filter(authority=authority).first()

        if not payment:
            return Response({
                "status": "error",
                "message": "پرداخت یافت نشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        gateway = Gateway.objects.filter(gateway_code="zarrinpal").first()

        if not gateway:
            return Response({
                "status": "error",
                "message": "درگاه پرداخت فعال یافت نشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        verified = payment.verify({
            'authority': authority,
            'status': payment_status
        })

        if verified and payment_status == "OK":
            with transaction.atomic():
                print("وارد اتمیک شدیم")
                if payment.transport:
                    print("پرداخت موفقیت امیز بود")
                    transport = TransportReq.objects.filter(pk=payment.transport.pk).first()
                    print("info is :", transport)
                    if transport:
                        transport.is_successful = True
                        transport.expire_time = timezone.now() + timedelta(hours=24)
                        transport.save()
                    print("درخواست اوکی شد")
                payment.is_paid = True
                print("درخواست پرداخت شد")
                payment.save()
            print("پرداخت ذخیره شد")
            return Response({
                "status": "success",
                "message": "پرداخت با موفقیت انجام شد."
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "پرداخت ناموفق بود."
        }, status=status.HTTP_400_BAD_REQUEST)



class AllLocationsApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
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



class CalculateRouteViewV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
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
            distance_km = calculate_distance(origin.latitude, origin.longitude, destination.latitude,
                                             destination.longitude)
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




class CreateTransportReqApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
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


class ApiTransportReqDeleteV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        transport_req_id = request.data.get('transport_req_id')  # دریافت ID محصول از داده‌های درخواست
        if not transport_req_id:
            return Response({"status": "error", "message": "transport ID is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        transport_req = get_object_or_404(TransportReq, id=transport_req_id)

        # بررسی مالکیت ترانزیت
        if transport_req.my_transport.user != request.user:
            return Response({"status": "error", "message": "You do not have permission to delete this transport"},
                            status=status.HTTP_403_FORBIDDEN)

        transport_req.delete()

        return Response({"status": "success", "message": "transport deleted successfully!"},
                        status=status.HTTP_200_OK)


class AllReqTransportByTypeApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

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
        now = timezone.now()
        all_req = TransportReq.objects.filter(my_transport__in=transport_req_ids, status=True, is_successful=True, expire_time__gt=now)

        paginator = PageNumberPagination()
        paginator.page_size = 12  # تعداد اقلام در هر صفحه
        result_page = paginator.paginate_queryset(all_req, request)
        serializer = TransportReqSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)


class AllReqTransportApiV1(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 16  # تعداد اقلام در هر صفحه
        # دریافت تاریخ و زمان فعلی
        now = timezone.now()
        all_my_req = TransportReq.objects.filter(status=True, expire_time__gt=now, is_successful=True).order_by(
            'id').all()
        result_page = paginator.paginate_queryset(all_my_req, request)
        serializer = TransportReqSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
