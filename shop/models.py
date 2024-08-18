import random
import datetime
from django.db import models
from django.contrib.auth import get_user_model as user_model
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children_category_shop', null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class MyShop(models.Model):
    ACTIVE = True
    INACTIVE = False
    STATUS_COMPANY = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    name_shop = models.CharField(max_length=32)
    administrator = models.CharField(max_length=48)
    mobile = models.CharField(max_length=20)
    code_posti = models.CharField(max_length=20)
    address = models.TextField()
    User = user_model()
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='%Y/%m/%d/myshop/')
    is_active = models.BooleanField(choices=STATUS_COMPANY, default=INACTIVE)
    created_time = models.DateTimeField(auto_now=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'MyShop'
        verbose_name_plural = "MyShops"

    def __str__(self):
        return self.name_shop


class Package(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    def __str__(self):
        return self.title


class Product(models.Model):

    ACTIVE = True
    INACTIVE = False

    VIJE_PRODUCT = (
        (ACTIVE, 'true'),
        (INACTIVE, 'false'),
    )
    User = user_model()
    user = models.ForeignKey(User, related_name='products_shop', on_delete=models.RESTRICT)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    my_shop = models.ForeignKey(MyShop, on_delete=models.PROTECT)
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    upc = models.BigIntegerField(unique=True)
    price = models.PositiveBigIntegerField()
    discount = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    vije = models.BooleanField(choices=VIJE_PRODUCT, default=INACTIVE)
    number_exist = models.PositiveIntegerField()
    number_send = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = "Products"

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('shop-single-web', args=[self.pk])

    @classmethod
    def add_product(cls, request, *args, **kwargs):
        result = "200"
        is_active = False
        upc = random.randint(11111111111111111, 99999999999999999)
        form = request.POST
        user = request.user

        category = form.get('category')
        brand = form.get('brand')
        discount = form.get('discount')

        number_exist = form.get('number_exist')
        if number_exist:
            number_exist = int(number_exist)
        else:
            result = "0"
            return result

        price = form.get('price')
        if price:
            price = int(price)
        else:
            result = "20"
            return result

        weight = form.get('weight')
        if weight:
            weight = int(weight)
        else:
            result = "30"
            return result

        description = form.get('description')

        warranty = form.get('warranty')
        numpic = form.get('numpic')
        numpic = int(numpic)+1

        new_product = Product(user=user, category=category, brand=brand, upc=upc, discount=discount,
                                  price=price, weight=weight, description=description,
                                  warranty=warranty, is_active=is_active, number_exist=number_exist)
        new_product.save()
        new_product_pk = new_product.pk
        if numpic >= 0:

            for i in range(numpic):
                print("request.FILES")
                if request.FILES.get(f'image{i}') is None:
                    pass
                else:
                    ali =request.FILES.get(f'image{i}')
                    new_image = ProductImage.add_images(request.FILES[f'image{i}'], new_product)

        return result

    def total_price(self):
        total_price_first = self.price * self.discount
        total_price_second = total_price_first/100
        total_price = self.price - total_price_second

        return round(total_price)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='shop/rebo/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images_shop')

    def __str__(self):
        return str(self.product)

    @classmethod
    def add_images(cls, image, product):
        new_image = ProductImage(image=image, product=product)
        new_image.save()
        return new_image


class Basket(models.Model):
    User = user_model()
    user = models.ForeignKey(User, related_name='baskets', on_delete=models.RESTRICT)
    basket_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Basket'
        verbose_name_plural = 'Baskets'

    def __str__(self):
        return self.user


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, related_name='baskets_line', on_delete=models.RESTRICT)
    Product = models.ForeignKey(Product, related_name='products', on_delete=models.RESTRICT)
    price = models.PositiveBigIntegerField()
    count = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total_price = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = 'BasketLine'
        verbose_name_plural = 'BasketLines'

    def __str__(self):
        return self.basket


class Invoice(models.Model):
    basket = models.ForeignKey(Basket, related_name='baskets_invoice', on_delete=models.RESTRICT)
    invoice_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return self.basket


class Transaction(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'pending'),
        ('FAILED', 'failed'),
        ('COMPLETE', 'complete'),
    )
    invoice = models.ForeignKey(Invoice, related_name='invoices', on_delete=models.RESTRICT)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return self.invoice


class Location(models.Model):
    name = models.CharField(max_length=48, null=True, blank=True)
    family = models.CharField(max_length=48)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    ostan = models.CharField(max_length=30)
    shahr = models.CharField(max_length=30)
    codeposti = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    User = user_model()
    user = models.ForeignKey(User, related_name='location', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def add_location(cls, request):

        form = request.POST
        user = request.user
        address = form.get('address')
        ostan = form.get('ostan')
        shahr = form.get('shahr')
        codeposti = form.get('codeposti')
        name = form.get('name')
        family = form.get('family')
        mobile = form.get('mobile')

        exist_location = Location.objects.filter(codeposti=codeposti).first()

        if exist_location:
            exist_location.codeposti = codeposti
            exist_location.save()
        else:
            new_location = Location(user=user, address=address, ostan=ostan, shahr=shahr, codeposti=codeposti,
                                    name=name, family=family, mobile=mobile)
            new_location.save()

    @classmethod
    def delete_location(cls, request, code_posti):
        form = request.POST
        user = request.user
        exist_location = Location.objects.filter(codeposti=code_posti).first()

        if exist_location:
            exist_location.remove()


