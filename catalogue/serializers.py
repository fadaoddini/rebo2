from rest_framework import serializers
from catalogue.models import Product, ProductImage, ProductAttribute, ProductAttributeValue, Brand, Category, \
    ProductType, ProductAttr
import datetime
import json
from datetime import timedelta
from django.db.models import Max, Min
from learn.models import Learn
import random

from login.serializers import MyUserSerializer


class ApiProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'value']


class ApiProductAttrSerializer(serializers.ModelSerializer):
    value = ProductAttributeValueSerializer()  # شامل مقادیر ویژگی‌ها

    class Meta:
        model = ProductAttr
        fields = ['type', 'attr', 'value']

    def create(self, validated_data):
        value_data = validated_data.pop('value', None)
        if value_data:
            value_instance, created = ProductAttributeValue.objects.get_or_create(**value_data)
            validated_data['value'] = value_instance
        return super().create(validated_data)


class SingleProductSerializer(serializers.ModelSerializer):
    images = ApiProductImageSerializer(many=True, read_only=True)
    user = MyUserSerializer()
    attrs = serializers.SerializerMethodField()  # برای گرفتن ویژگی‌ها به صورت خاص
    lable = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    top_price_bid = serializers.SerializerMethodField()
    count_bid = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'upc', 'weight', 'price', 'description', 'warranty', 'lable', 'name', 'top_price_bid', 'count_bid',
                  'is_active', 'images', 'attrs', 'user', 'create_time', 'expire_time']

    def get_attrs(self, obj):
        attrs = ProductAttr.objects.filter(product=obj)
        result = []
        for attr in attrs:
            result.append({
                "attr": attr.attr.title if attr.attr else None,  # نمایش title ویژگی
                "value": attr.value.value
            })
        return result

    def get_lable(self, obj):
        return obj.product_type.title

    def get_name(self, obj):
        return obj.product_type.name

    def get_top_price_bid(self, obj):
        top_price_bid = obj.bids.aggregate(Max('price'))['price__max']
        return top_price_bid if top_price_bid is not None else 0

    def get_count_bid(self, obj):
        return obj.bids.count()

class SellSingleProductSerializer(serializers.ModelSerializer):
    images = ApiProductImageSerializer(many=True, read_only=True)
    user = MyUserSerializer()
    attrs = serializers.SerializerMethodField()  # برای گرفتن ویژگی‌ها به صورت خاص
    lable = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    top_price_bid = serializers.SerializerMethodField()
    count_bid = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'upc', 'weight', 'price', 'description', 'warranty', 'lable', 'name', 'top_price_bid', 'count_bid',
                  'is_active', 'images', 'attrs', 'user', 'create_time', 'expire_time']

    def get_attrs(self, obj):
        attrs = ProductAttr.objects.filter(product=obj)
        result = []
        for attr in attrs:
            result.append({
                "attr": attr.attr.title if attr.attr else None,  # نمایش title ویژگی
                "value": attr.value.value
            })
        return result

    def get_lable(self, obj):
        return obj.product_type.title

    def get_name(self, obj):
        return obj.product_type.name

    def get_top_price_bid(self, obj):
        top_price_bid = obj.bids.aggregate(Max('price'))['price__max']
        return top_price_bid if top_price_bid is not None else 0

    def get_count_bid(self, obj):
        return obj.bids.count()



class BuySingleProductSerializer(serializers.ModelSerializer):
    images = ApiProductImageSerializer(many=True, read_only=True)
    user = MyUserSerializer()
    attrs = serializers.SerializerMethodField()  # برای گرفتن ویژگی‌ها به صورت خاص
    lable = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    top_price_bid = serializers.SerializerMethodField()
    count_bid = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'upc', 'weight', 'price', 'description', 'warranty', 'lable', 'name', 'top_price_bid', 'count_bid',
                  'is_active', 'images', 'attrs', 'user', 'create_time', 'expire_time']

    def get_attrs(self, obj):
        attrs = ProductAttr.objects.filter(product=obj)
        result = []
        for attr in attrs:
            result.append({
                "attr": attr.attr.title if attr.attr else None,  # نمایش title ویژگی
                "value": attr.value.value
            })
        return result

    def get_lable(self, obj):
        return obj.product_type.title

    def get_name(self, obj):
        return obj.product_type.name

    def get_top_price_bid(self, obj):
        top_price_bid = obj.bids.aggregate(Min('price'))['price__min']
        return top_price_bid if top_price_bid is not None else 0

    def get_count_bid(self, obj):
        return obj.bids.count()



class ApiProductSerializer(serializers.ModelSerializer):
    images = ApiProductImageSerializer(many=True, required=False)
    attrs = serializers.JSONField(required=False)  # استفاده از JSONField برای ویژگی‌های محصول

    class Meta:
        model = Product
        fields = ['sell_buy', 'product_type', 'price', 'weight', 'description', 'warranty', 'is_active',
                  'expire_time', 'images', 'attrs']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        attrs_data = validated_data.pop('attrs', [])

        # مدیریت expire_time
        expire_time_days = validated_data.pop('expire_time', 0)
        if expire_time_days:
            expire_time = datetime.datetime.now() + timedelta(days=int(expire_time_days))
            validated_data['expire_time'] = expire_time
        else:
            validated_data['expire_time'] = None

        validated_data.setdefault('is_active', True)
        product = Product.objects.create(**validated_data)

        # ایجاد تصاویر
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        # پردازش ویژگی‌ها
        if isinstance(attrs_data, str):
            attrs_data = json.loads(attrs_data)  # تبدیل رشته JSON به لیست دیکشنری‌ها

        for attr_data in attrs_data:
            ApiProductAttrSerializer().create({**attr_data, 'product': product})

        return product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'title', 'image']
    # سریالایزر برای تبدیل مدل Category به JSON و بالعکس استفاده می‌شود.
    # فیلدهای 'id' و 'name' را شامل می‌شود.


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'title', 'name', 'image']
    # سریالایزر برای تبدیل مدل ProductType به JSON و بالعکس استفاده می‌شود.
    # فیلدهای 'id' و 'title' را شامل می‌شود.


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'title', 'product_type']
    # سریالایزر برای تبدیل مدل ProductAttribute به JSON و بالعکس استفاده می‌شود.
    # فیلدهای 'id'، 'title' و 'product_type' را شامل می‌شود.


class CategoryTypeSerializer(serializers.Serializer):
    category = serializers.CharField()
    cat_id = serializers.IntegerField()
    types = serializers.SerializerMethodField()

    def get_types(self, obj):
        types = obj['types']
        return TypesSerializer2(types, many=True).data



class TypesSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id', 'name', 'title', 'image')



class TypesSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    cat_id = serializers.SerializerMethodField()

    class Meta:
        model = ProductType
        fields = ('id', 'name', 'title', 'image', 'category', 'cat_id')

    def get_category(self, obj):
        name = obj.category
        return name.name


    def get_cat_id(self, obj):
        name = obj.category
        return name.id


class ProductSellSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    upc = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    name_type = serializers.SerializerMethodField()
    attr_value = serializers.SerializerMethodField()
    finished_time = serializers.SerializerMethodField()
    top_price_bid = serializers.SerializerMethodField()
    count_bid = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'upc', 'weight', 'price', 'name_type', 'product_type', 'sell_buy', 'top_price_bid', 'count_bid',
                  'is_active', 'is_successful', 'user', 'description', 'create_time', 'finished_time', 'images', 'attr_value')

    def get_user(self, obj):
        name2 = obj.user.first_name + " " + obj.user.last_name
        return name2

    def get_upc(self, obj):
            upc = str(obj.upc)
            return upc

    def get_name_type(self, obj):
        id_type = obj.product_type
        return id_type.title

    def get_count_bid(self, obj):
        return obj.bids.count()

    def get_top_price_bid(self, obj):

        top_price_bid = obj.bids.aggregate(Max('price'))['price__max']
        return top_price_bid if top_price_bid is not None else 0

    def get_finished_time(self, obj):
        finish_time = obj.expire_time
        now = datetime.datetime.now()
        days_left = finish_time - now  # seconds
        # rooz = days_left/86400

        return finish_time

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(), many=True).data

    def get_attr_value(self, obj):
        result = []
        id_type = obj.product_type
        attrs = ProductAttribute.objects.filter(product_type=id_type)
        for attr in attrs:
            value = ProductAttributeValue.objects.filter(product_attribute=attr.id).first()
            # result[attr.title] = value.value
            result.append({
                "key": attr.title,
                "value": value.value
                           })

        return result


class ProductSingleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    name_type = serializers.SerializerMethodField()
    attr_value = serializers.SerializerMethodField()
    finished_time = serializers.SerializerMethodField()
    learn = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'upc', 'weight', 'price', 'name_type', 'product_type',
                  'is_active', 'user', 'description', 'create_time', 'finished_time', 'images', 'attr_value', 'learn')

    def get_user(self, obj):
        name2 = obj.user.first_name + " " + obj.user.last_name
        return name2

    def get_learn(self, obj):
        result = []
        type = obj.product_type
        learns = Learn.objects.filter(type=type)
        for learn in learns:
            result.append({
                "id": learn.id,
                "title": learn.title,
                "price": learn.price,
                "image": learn.image.url,
                "auther": learn.auther
                })
        return result

    def get_name_type(self, obj):
        id_type = obj.product_type
        return id_type.title

    def get_finished_time(self, obj):
        sabt_shode = obj.create_time
        finish_time = sabt_shode+timedelta(days=30)
        now = datetime.datetime.now()
        days_left = finish_time - now  # seconds
        rooz = days_left/86400
        return finish_time

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(), many=True).data

    def get_attr_value(self, obj):
        result = []
        id_type = obj.product_type
        attrs = ProductAttribute.objects.filter(product_type=id_type)
        for attr in attrs:
            value = ProductAttributeValue.objects.filter(product_attribute=attr.id).first()
            # result[attr.title] = value.value
            result.append({
                "key": attr.title,
                "value": value.value
                           })

        return result


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', )