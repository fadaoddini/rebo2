from django.db import models
from login.models import MyUser
from django.contrib import messages


class Info(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_INFO = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    TAEED = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    image = models.ImageField(upload_to='%Y/%m/%d/users/', null=True, blank=True)
    shaba = models.CharField(max_length=24, unique=True, null=True, blank=True)
    image_shaba = models.ImageField(upload_to='%Y/%m/%d/shabas/', null=True, blank=True)
    codemeli = models.CharField(max_length=24, unique=True, null=True, blank=True)
    okmeli = models.BooleanField(choices=TAEED, default=INACTIVE)
    okbank = models.BooleanField(choices=TAEED, default=INACTIVE)
    image_codemeli = models.ImageField(upload_to='%Y/%m/%d/codemelis/', null=True, blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='info')
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(choices=STATUS_INFO, default=INACTIVE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Farmer(models.Model):
    ACTIVE = True
    INACTIVE = False
    TAEED = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    lat = models.CharField(max_length=40, null=True, blank=True)
    long = models.CharField(max_length=40, null=True, blank=True)
    number_tree = models.CharField(max_length=40, null=True, blank=True)
    score = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to='%Y/%m/%d/farmer/', null=True, blank=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='farmer')
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(choices=TAEED, default=INACTIVE)

    def __str__(self):
        return str(self.user)


class Storage(models.Model):
    ACTIVE = True
    INACTIVE = False
    TAEED = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    ACCEPT = (
        (ACTIVE, 'yes'),
        (INACTIVE, 'no'),
    )

    lat = models.CharField(max_length=40, null=True, blank=True)
    long = models.CharField(max_length=40, null=True, blank=True)
    capacity = models.CharField(max_length=40, null=True, blank=True)
    score = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to='%Y/%m/%d/farmer/', null=True, blank=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='storage')
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_accept = models.BooleanField(choices=ACCEPT, default=INACTIVE)
    is_active = models.BooleanField(choices=TAEED, default=INACTIVE)

    def __str__(self):
        return str(self.user)


class Broker(models.Model):
    ACTIVE = True
    INACTIVE = False
    TAEED = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    score = models.PositiveBigIntegerField(default=0)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='broker')
    image = models.ImageField(upload_to='%Y/%m/%d/broker/', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(choices=TAEED, default=INACTIVE)

    def __str__(self):
        return str(self.user)


class ServiceType(models.Model):
    title = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'ServiceType'
        verbose_name_plural = 'ServiceTypes'

    def __str__(self):
        return self.title


class Service(models.Model):
    ACTIVE = True
    INACTIVE = False
    TAEED = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,
                                             related_name='services')
    num = models.PositiveBigIntegerField(default=1)
    score = models.PositiveBigIntegerField(default=0)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='service')
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(choices=TAEED, default=INACTIVE)

    def __str__(self):
        return f"({self.user}):{self.num}"



