from django.db import models
from django.contrib.auth import get_user_model as user_model
import math


class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class TransportType(models.Model):

    title = models.CharField(max_length=32, blank=True, null=True)
    image = models.ImageField(upload_to='%Y/%m/%d/transport/type/', null=True, blank=True)

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

    def __str__(self):
        return self.title


class Transport(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_TRANSPORT = (
        (ACTIVE, 'true'),
        (INACTIVE, 'false'),
    )
    car_name = models.CharField(max_length=42, blank=True, null=True)
    User = user_model()
    user = models.ForeignKey(User, related_name='transports', on_delete=models.RESTRICT)
    transport_type = models.ForeignKey(TransportType, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='%Y/%m/%d/transport/car/', null=True, blank=True)
    pelak = models.CharField(max_length=10)
    iran = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    status = models.BooleanField(choices=STATUS_TRANSPORT, default=ACTIVE)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    expire_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Transport'
        verbose_name_plural = "Transports"

    def __str__(self):
        return f"{self.car_name}"


class TransportReq(models.Model):
    STATUS_CHOICES = (
        ('ONE_ME', 'one me'),
        ('UP_TO_YOU', 'up to you'),
    )

    ACTIVE = True
    INACTIVE = False

    STATUS_REQ = (
        (ACTIVE, 'true'),
        (INACTIVE, 'false'),
    )
    origin = models.ForeignKey(Location, related_name='origin_requests', on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey(Location, related_name='destination_requests', on_delete=models.SET_NULL, null=True)
    distance = models.CharField(max_length=42, blank=True, null=True)
    price = models.PositiveBigIntegerField()
    description = models.TextField(blank=True)
    status = models.BooleanField(choices=STATUS_REQ, default=ACTIVE)
    barnameh = models.CharField(max_length=100, choices=STATUS_CHOICES, default='ONE_ME')
    my_transport = models.ForeignKey(Transport, related_name='transportreqs', on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    expire_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'TransportReq'
        verbose_name_plural = "TransportReqs"

    def __str__(self):
        return f"{self.origin} - {self.destination}"


class PriceList(models.Model):
    min_cost_per_one_ton = models.PositiveIntegerField()
    max_cost_per_one_ton = models.PositiveIntegerField()
    min_cost_per_one_km = models.PositiveIntegerField()
    max_cost_per_one_km = models.PositiveIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.min_cost_per_one_ton} - {self.max_cost_per_one_ton} - {self.min_cost_per_one_km} - {self.max_cost_per_one_km}"


class RouteMetrics(models.Model):
    origin = models.ForeignKey(Location, related_name='origin_routes', on_delete=models.CASCADE)
    destination = models.ForeignKey(Location, related_name='destination_routes', on_delete=models.CASCADE)
    transport_capacity = models.PositiveIntegerField(null=True, blank=True)  # ظرفیت خودرو به تن
    distance_km = models.IntegerField(blank=True, null=True)  # ذخیره به صورت عدد صحیح
    min_duration_hours = models.IntegerField(blank=True, null=True)  # ذخیره به صورت عدد صحیح
    max_duration_hours = models.IntegerField(blank=True, null=True)  # ذخیره به صورت عدد صحیح
    min_cost = models.BigIntegerField(blank=True, null=True)  # هزینه به صورت ریال
    max_cost = models.BigIntegerField(blank=True, null=True)  # هزینه به صورت ریال

    # Define cost per ton in Rials (Iranian currency)
    min_cost_per_one_ton = 20000  # هزینه به ریال برای هر تن
    max_cost_per_one_ton = 30000  # هزینه به ریال برای هر تن

    def __str__(self):
        return f'{self.origin} to {self.destination}'

    def save(self, *args, **kwargs):
        # Calculate distance and costs if both origin and destination are set
        if self.origin and self.destination:
            self.distance_km = self.calculate_distance()
            self.min_duration_hours = round(self.distance_km / 100)  # Example calculation
            self.max_duration_hours = round(self.distance_km / 50)  # Example calculation

            # Calculate min_cost and max_cost based on the cost per ton and capacity
            if self.transport_capacity:
                self.min_cost = round(self.distance_km * self.min_cost_per_one_ton * self.transport_capacity / 1000) * 1000
                self.max_cost = round(self.distance_km * self.max_cost_per_one_ton * self.transport_capacity / 1000) * 1000
            else:
                self.min_cost = round(self.distance_km * self.min_cost_per_one_ton / 1000) * 1000
                self.max_cost = round(self.distance_km * self.max_cost_per_one_ton / 1000) * 1000

        super(RouteMetrics, self).save(*args, **kwargs)

    def calculate_distance(self):
        R = 6371  # Radius of Earth in kilometers
        dlat = math.radians(self.destination.latitude - self.origin.latitude)
        dlon = math.radians(self.destination.longitude - self.origin.longitude)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(self.origin.latitude)) * math.cos(
            math.radians(self.destination.latitude)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c)  # گرد کردن مسافت به نزدیک‌ترین کیلومتر


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c)  # گرد کردن مسافت به نزدیک‌ترین کیلومتر