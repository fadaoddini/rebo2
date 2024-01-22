import random
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user_model
from django.db import models, transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class ProductType(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):

    title = models.CharField(max_length=32)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='attributes')

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Product(models.Model):
    SELL = 1
    BUY = 2

    TYPES_SELL_OR_BUY = (
        (SELL, "sell"),
        (BUY, "buy"),
    )
    ACTIVE = True
    INACTIVE = False

    WARRANTY_PRODUCT = (
        (ACTIVE, 'true'),
        (INACTIVE, 'false'),
    )
    User = user_model()
    user = models.ForeignKey(User, related_name='products', on_delete=models.RESTRICT)
    sell_buy = models.PositiveSmallIntegerField(default=SELL, choices=TYPES_SELL_OR_BUY)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    upc = models.BigIntegerField(unique=True)
    price = models.PositiveBigIntegerField()
    weight = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    warranty = models.BooleanField(choices=WARRANTY_PRODUCT, default=INACTIVE)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    expire_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = "Products"

    def __str__(self):
        return self.description

    def get_time(self):
        if self.expire_time > datetime.datetime.now():
            return True
        else:
            return False

    @classmethod
    def add_product(cls, request, sell_buy, *args, **kwargs):
        result = "200"
        is_active = False
        upc = random.randint(11111111111111111, 99999999999999999)
        form = request.POST
        user = request.user

        days = form.get('expire_time')
        expire_time1 = datetime.datetime.now() + datetime.timedelta(days=int(days))
        expire_time = datetime.datetime.strftime(expire_time1, '%Y-%m-%d')
        product_type = form.get('product_type')
        if product_type != "None":
            pass
        else:
            result = "40"
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
        product_type_model = ProductType.objects.filter(pk=product_type).first()

        with transaction.atomic():
            new_product = Product(user=user, sell_buy=sell_buy, product_type=product_type_model, upc=upc,
                                  price=price, weight=weight, description=description,
                                  warranty=warranty, is_active=is_active, expire_time=expire_time)
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

            attributes_model = ProductAttribute.objects.filter(product_type_id=product_type)
            for attr in attributes_model:
                pk_attr = attr.pk
                attr_val = form.get('attrval' + str(pk_attr))
                pk_attr_model = ProductAttribute.objects.filter(pk=pk_attr).first()
                attr_val_model = ProductAttributeValue.objects.filter(pk=attr_val).first()
                # ADD ATTR PRODUCT TABLE
                finish_gam = ProductAttr(type=product_type_model, attr=pk_attr_model, value=attr_val_model,
                                         product=new_product)
                finish_gam.save()
            result = "100"
        return result

    def total_price(self):
        total_price = self.price * self.weight
        return round(total_price/10)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.product)

    @classmethod
    def add_images(cls, image, product):
        new_image = ProductImage(image=image, product=product)
        new_image.save()
        return new_image


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.PROTECT, related_name='values')
    value = models.CharField(max_length=48)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.product_attribute}):{self.value}"


class ProductAttr(models.Model):
    type = models.ForeignKey(ProductType, on_delete=models.PROTECT, null=True, blank=True)
    attr = models.ForeignKey(ProductAttribute, on_delete=models.PROTECT, null=True, blank=True)
    value = models.ForeignKey(ProductAttributeValue, on_delete=models.PROTECT,
                              related_name='values', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attrs', null=True, blank=True)

    def __str__(self):
        return str(self.product)

