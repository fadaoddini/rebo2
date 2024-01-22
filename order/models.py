import json
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model as user_model

from order.utils import zpal_request_handler, zpal_payment_checker


class Gateway(models.Model):
    FUNCTION_ZARRINPAL = 'zarrinpal'
    FUNCTION_MELAT = 'melat'
    FUNCTION_MELI = 'meli'
    GATEWAY_FUNCTION = (
        (FUNCTION_ZARRINPAL, 'zarrinpal'),
        (FUNCTION_MELAT, 'melat'),
        (FUNCTION_MELI, 'meli'),

    )
    title = models.CharField(max_length=100)
    gateway_request_url = models.CharField(max_length=150, null=True, blank=True)
    gateway_verify_url = models.CharField(max_length=150, null=True, blank=True)
    gateway_code = models.CharField(max_length=12, choices=GATEWAY_FUNCTION, default=FUNCTION_ZARRINPAL)
    is_enable = models.BooleanField(default=True)
    auth_data = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'

    def __str__(self):
        return self.title

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_ZARRINPAL: zpal_request_handler,
            self.FUNCTION_MELAT: None,
            self.FUNCTION_MELI: None,
        }
        return handlers[self.gateway_code]

    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_ZARRINPAL: zpal_payment_checker,
            self.FUNCTION_MELAT: None,
            self.FUNCTION_MELI: None,
        }
        return handlers[self.gateway_code]

    @property
    def credentials(self):
        return json.loads(self.auth_data)


# Create your models here.
class Payment(models.Model):
    faktor_number = models.UUIDField(unique=True)
    amount = models.PositiveIntegerField(editable=True)
    gateway = models.CharField(max_length=40)
    is_paid = models.BooleanField(default=False)
    payment_log = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    authority = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.faktor_number.hex

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_paid = self.is_paid

    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()
        if handler is not None:
            return handler(self.gateway, self)

    @property
    def title(self):
        return "Instant payment"

    def status_changed(self):
        return self.is_paid != self._b_is_paid

    def verify(self, data):
        handler = self.gateway.get_verify_handler()
        if not self.is_paid and handler is not None:
            handler(self, data)
        return self.is_paid

    def get_gateway(self):
        gateway = Gateway.objects.filter(is_enable=True).first()
        return gateway.gateway_code

    def save_log(self, data, scope='Request handler', save=True):
        generated_log = "[{}][{}] {}\n".format(timezone.now(), scope, data)
        if self.payment_log != '':
            self.payment_log += generated_log
        else:
            self.payment_log = generated_log
        if save:
            self.save()

    @classmethod
    def create_payment(cls, authority, amount, user):
        return cls.objects.create(
            faktor_number=uuid.uuid4(),
            authority=authority,
            amount=amount,
            gateway="zarinpal",
            user=user
        )


class Order(models.Model):
    User = user_model()
    user = models.ForeignKey(User, related_name='order', on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

