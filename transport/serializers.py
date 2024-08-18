from rest_framework import serializers
from django.templatetags.static import static
from transport.models import TransportReq, TransportType, Transport, Location, RouteMetrics


class TransportSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = Transport
        fields = ('id', 'car_name', 'transport_type', 'pelak', 'iran', 'mobile', 'capacity', 'description',
                  'status', 'user', 'image', 'create_time', 'expire_time')

    def get_user(self, obj):
        name2 = obj.user.first_name + " " + obj.user.last_name
        return name2

    def get_mobile(self, obj):
        mobile = obj.user.mobile
        return mobile


class TransportTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransportType
        fields = ('id', 'title', 'image')


class MyTransportSerializer(serializers.ModelSerializer):
    mobile = serializers.SerializerMethodField()
    transport_type = serializers.SerializerMethodField()
    class Meta:
        model = Transport
        fields = ('car_name', 'capacity', 'mobile', 'transport_type', 'description')

    def get_mobile(self, obj):
        return f"{obj.user.mobile}"

    def get_transport_type(self, obj):
        return f"{obj.transport_type.title}"


class TransportReqSerializer(serializers.ModelSerializer):
    my_transport = MyTransportSerializer()  # استفاده از MyTransportSerializer
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    pelak = serializers.SerializerMethodField()
    iran = serializers.SerializerMethodField()
    origin = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = TransportReq
        fields = ('id', 'user', 'origin', 'image', 'destination', 'distance', 'price', 'description',
                  'status', 'barnameh', 'my_transport', 'create_time', 'expire_time', 'pelak', 'iran')

    def get_user(self, obj):
        return f"{obj.my_transport.user.first_name} {obj.my_transport.user.last_name}"

    def get_image(self, obj):
        if obj.my_transport and obj.my_transport.image:
            return obj.my_transport.image.url
        return static('index/img/nopic.png')  # مسیر به تصویر پیش‌فرض

    def get_pelak(self, obj):
        return obj.my_transport.pelak

    def get_price(self, obj):
        price = obj.price
        total_price = round(price * 1000000)/1000000
        return total_price

    def get_iran(self, obj):
        return obj.my_transport.iran

    def get_origin(self, obj):
        if obj.origin:
            return obj.origin.name
        return None

    def get_destination(self, obj):
        if obj.destination:
            return obj.destination.name
        return None


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class RouteMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteMetrics
        fields = '__all__'