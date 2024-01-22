import sys

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Sum, Q, Count
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model as user_model


class Company(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_COMPANY = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    User = user_model()
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    name = models.CharField(max_length=48)
    image = models.ImageField(upload_to='%Y/%m/%d/companies/')
    is_active = models.BooleanField(choices=STATUS_COMPANY, default=INACTIVE)
    created_time = models.DateTimeField(auto_now=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f"{self.name}"


class Location(models.Model):
    name = models.CharField(max_length=48)
    address = models.TextField()
    company = models.ForeignKey(Company, related_name='location', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"{self.name}"


class TypeDates(models.Model):

    KG = 1
    NUMBER = 2
    LITER = 3

    VALUE_TYPE_CHOICES = (
        (KG, 'kg'),
        (NUMBER, 'number'),
        (LITER, 'liter'),
    )

    name = models.CharField(max_length=48)
    type = models.PositiveSmallIntegerField(choices=VALUE_TYPE_CHOICES, default=KG)
    company = models.ForeignKey(Company, related_name='type_dates', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'TypeDate'
        verbose_name_plural = 'TypeDates'

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    name = models.CharField(max_length=48, null=True, blank=True)
    family = models.CharField(max_length=48)
    mobile = models.CharField(max_length=20)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    company = models.ForeignKey(Company, related_name='customer', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.name} {self.family}"


class Driver(models.Model):
    name = models.CharField(max_length=48, null=True, blank=True)
    family = models.CharField(max_length=48)
    mobile = models.CharField(max_length=20)
    plaque = models.PositiveIntegerField()
    vasat = models.CharField(max_length=10)
    iran = models.PositiveSmallIntegerField()
    company = models.ForeignKey(Company, related_name='driver', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return f"{self.family}"


class Staff(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_TYPE_CHOICES = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )

    ACTIVE = True
    INACTIVE = False

    INSURANCE_TYPE_CHOICES = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )

    YES = True
    NO = False

    INSURANCE_STATUS_CHOICES = (
        (YES, 'yes'),
        (NO, 'no'),
    )
    IS_MARRIED_CHOICES = (
        (YES, 'yes'),
        (NO, 'no'),
    )

    OFFICIAL = 1
    WORKER = 2
    SUPERVISOR = 3

    ROLE_TYPE_CHOICES = (
        (OFFICIAL, 'official'),
        (WORKER, 'worker'),
        (SUPERVISOR, 'supervisor'),
    )
    MAN = 1
    WOMAN = 2
    JENS_TYPE_CHOICES = (
        (MAN, 'man'),
        (WOMAN, 'woman'),
    )

    location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='location')
    name = models.CharField(max_length=48, null=True, blank=True)
    family = models.CharField(max_length=48)
    mobile = models.CharField(max_length=48, default=0)
    codemeli = models.CharField(max_length=48, default=0)
    age = models.CharField(max_length=48, default=0)
    jens = models.PositiveSmallIntegerField(choices=JENS_TYPE_CHOICES, null=True, blank=True)
    is_married = models.BooleanField(choices=IS_MARRIED_CHOICES, null=True, blank=True)
    card_number = models.CharField(max_length=48, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_TYPE_CHOICES, default=WORKER)
    insurance = models.BooleanField(choices=INSURANCE_TYPE_CHOICES, default=INACTIVE)

    insurance_status = models.BooleanField(choices=INSURANCE_STATUS_CHOICES, default=YES)
    fix_salary = models.BigIntegerField(default=0)
    salon = models.PositiveSmallIntegerField(default=1)
    status = models.BooleanField(choices=STATUS_TYPE_CHOICES, default=ACTIVE)

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

    def __str__(self):
        return f"{self.name} {self.family}"


class Warehouse(models.Model):
    IN = 1
    OUT = 2
    TRANSFER_IN = 3
    TRANSFER_OUT = 4

    TRANSFER_TYPE_CHOICES = (
        (IN, 'in'),
        (OUT, 'out'),
        (TRANSFER_IN, 'transfer in'),
        (TRANSFER_OUT, 'transfer out'),
    )

    positive_transfer = Sum(
        'warehouse__quantity',
        filter=Q(warehouse__transfer_type__in=[1, 3])
    )

    negative_transfer = Sum(
        'warehouse__quantity',
        filter=Q(warehouse__transfer_type__in=[2, 4])
    )

    KG = 1
    NUMBER = 2
    LITER = 3

    VALUE_TYPE_CHOICES = (
        (KG, 'kg'),
        (NUMBER, 'number'),
        (LITER, 'liter'),
    )

    typedate = models.ForeignKey(TypeDates, related_name='typedate_warehouse', on_delete=models.RESTRICT)
    company = models.ForeignKey(Company, related_name='company_warehouse', on_delete=models.RESTRICT)
    customer = models.ForeignKey(Customer, related_name='warehouse', on_delete=models.RESTRICT)
    driver = models.ForeignKey(Driver, related_name='driver_warehouse', on_delete=models.RESTRICT)
    transfer_type = models.PositiveSmallIntegerField(choices=TRANSFER_TYPE_CHOICES, default=IN)
    value_type = models.PositiveSmallIntegerField(choices=VALUE_TYPE_CHOICES, default=KG)
    quantity = models.BigIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = "Warehouses"

    def __str__(self):
        return f"{self.customer} - {self.typedate} - {self.quantity} "

    @classmethod
    def get_report(cls):
        customers = Customer.objects.all().annotate(
            transfer_count=Count('warehouse__id'),
            balance=Coalesce(cls.positive_transfer, 0) - Coalesce(cls.negative_transfer, 0)
        )
        return customers

    @classmethod
    def get_report_by_customer(cls, pk):
        """show one user and show balance"""
        customer = Customer.objects.filter(id=pk).aggregate(
            transaction_count=Count('warehouse__id'),
            balance=Coalesce(cls.positive_transfer, 0) - Coalesce(cls.negative_transfer, 0)
        )
        return customer

    @classmethod
    def customer_balance_quantity(cls, customer, typedate):
        positive_transfer = Sum(
            'quantity',
            filter=Q(transfer_type__in=[1, 3])
        )
        negative_transfer = Sum(
            'quantity',
            filter=Q(transfer_type__in=[2, 4])
        )
        customer_balance_quantity_result = customer.warehouse.filter(typedate=typedate).aggregate(
            balance=Coalesce(positive_transfer, 0) - Coalesce(negative_transfer, 0)
        )

        return customer_balance_quantity_result.get('balance', 0)

    @classmethod
    def customer_balance_quantity_test(cls, customer, typedate):
        customer = Customer.objects.get(id=customer)
        typedate = TypeDates.objects.get(id=typedate)
        balance = Warehouse.customer_balance_quantity(customer, typedate)

        return balance


class CustomerBalance(models.Model):
    customer = models.ForeignKey(Customer, related_name='balance_records', on_delete=models.RESTRICT)
    typedate = models.ForeignKey(TypeDates, related_name='balance_type', on_delete=models.RESTRICT)
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = "Balances"

    def __str__(self):
        return f"{self.customer} - {self.balance} - {self.created_time}"

    @classmethod
    def record_customer_by_id_balance(cls, pk, typedate):

        customer = Customer.objects.get(id=pk)
        typedate = TypeDates.objects.get(id=typedate)
        balance = Warehouse.customer_balance_quantity(customer, typedate)

        instance = cls.objects.create(
            customer=customer,
            typedate=typedate,
            balance=balance
        )
        cls.record_all_customer_balance()
        return instance

    @classmethod
    def record_customer_balance(cls, customer, typedate):

        positive_transfer = Sum(
            'quantity',
            filter=Q(transfer_type__in=[1, 3])
        )
        negative_transfer = Sum(
            'quantity',
            filter=Q(transfer_type__in=[2, 4])
        )

        customer_balance_quantity = customer.warehouse.filter(typedate=typedate).aggregate(
            balance=Coalesce(positive_transfer, 0) - Coalesce(negative_transfer, 0)
        )
        instance = cls.objects.create(
            customer=customer,
            typedate=typedate,
            balance=customer_balance_quantity['balance']
        )
        return instance

    @classmethod
    def record_all_customer_balance(cls):
        cls.objects.all().delete()
        customers = Customer.objects.all()
        typedates = TypeDates.objects.all()
        for customer in customers:
            for typedate in typedates:
                cls.record_customer_balance(customer, typedate)


class TransferWarehouse(models.Model):
    sender_transfer = models.OneToOneField(
        Warehouse, related_name='sender_transfer', on_delete=models.RESTRICT
    )
    received_transfer = models.OneToOneField(
        Warehouse, related_name='received_transfer', on_delete=models.RESTRICT
    )
    typedate = models.ForeignKey(TypeDates, related_name='type_transfer', on_delete=models.RESTRICT)

    quantity = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_transfer} - {self.quantity} - {self.received_transfer}"

        return customer_balance_all_type.get('balance', 0)

    @classmethod
    def transfer(cls, sender, receiver, typedate, quantity, driver):

        if Warehouse.customer_balance_quantity_test(sender, typedate) < quantity:
            return "transfer not Allowed, insufficient balance"

        sender = Customer.objects.filter(id=sender).first()
        receiver = Customer.objects.filter(id=receiver).first()
        typedate = TypeDates.objects.filter(id=typedate).first()
        company = sender.company
        value_type = typedate.type
        driver = Driver.objects.filter(id=driver).first()

        with transaction.atomic():
            send_transfer = Warehouse.objects.create(
                customer=sender, transfer_type=Warehouse.TRANSFER_IN, quantity=quantity,
                typedate=typedate, company=company, value_type=value_type, driver=driver
            )
            received_transfer = Warehouse.objects.create(
                customer=receiver, transfer_type=Warehouse.TRANSFER_OUT, quantity=quantity,
                typedate=typedate, company=company, value_type=value_type, driver=driver
            )

            instance = cls.objects.create(
                sender_transfer=send_transfer,
                received_transfer=received_transfer,
                quantity=quantity, typedate=typedate
            )
            CustomerBalance.record_all_customer_balance()
        return instance







