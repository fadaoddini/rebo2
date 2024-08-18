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
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT)
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
        if self.expire_time and self.expire_time > timezone.now():
            return True
        return False

    @classmethod
    def add_product(cls, request, sell_buy, *args, **kwargs):
        result = "200"
        is_active = False
        upc = random.randint(11111111111111111, 99999999999999999)
        form = request.POST
        user = request.user

        days = form.get('expire_time')
        if days:
            expire_time1 = timezone.now() + datetime.timedelta(days=int(days))
            expire_time = expire_time1
        else:
            result = "30"  # or other error code
            return result

        product_type = form.get('product_type')
        if not product_type:
            result = "40"
            return result

        price = form.get('price')
        weight = form.get('weight')
        description = form.get('description')
        warranty = form.get('warranty') == 'True'

        product_type_model = ProductType.objects.filter(pk=product_type).first()
        if not product_type_model:
            result = "40"
            return result

        with transaction.atomic():
            new_product = Product(user=user, sell_buy=sell_buy, product_type=product_type_model, upc=upc,
                                  price=price, weight=weight, description=description,
                                  warranty=warranty, is_active=is_active, expire_time=expire_time)
            new_product.save()
            new_product_pk = new_product.pk
            numpic = int(form.get('numpic', 0))
            for i in range(numpic):
                image = request.FILES.get(f'image{i}')
                if image:
                    ProductImage.add_images(image, new_product)

            attributes_model = ProductAttribute.objects.filter(product_type_id=product_type)
            for attr in attributes_model:
                attr_val = form.get(f'attrval{attr.pk}')
                if attr_val:
                    attr_val_model = ProductAttributeValue.objects.filter(pk=attr_val).first()
                    ProductAttr(type=product_type_model, attr=attr, value=attr_val_model, product=new_product).save()
            result = "100"
        return result


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

