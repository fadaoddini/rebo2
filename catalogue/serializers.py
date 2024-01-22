from rest_framework import serializers
from catalogue.models import Product, ProductImage, ProductAttribute, ProductAttributeValue, Brand, Category
import datetime
from datetime import timedelta
import math

from learn.models import Learn


class ProductSellSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    name_type = serializers.SerializerMethodField()
    attr_value = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'upc', 'title', 'brand', 'brand_name', 'category', 'category_name', 'weight', 'price', 'name_type', 'product_type',
                  'is_active', 'user', 'description', 'create_time', 'days_left', 'images', 'attr_value')

    def get_user(self, obj):
        name2 = obj.user.info.name + " " + obj.user.info.family
        return name2

    def get_name_type(self, obj):
        id_type = obj.product_type
        return id_type.title

    def get_brand_name(self, obj):
        brand_name = obj.brand.name
        return brand_name

    def get_category_name(self, obj):
        category_name = obj.category.name
        return category_name

    def get_days_left(self, obj):
        sabt_shode = obj.create_time
        finish_time = sabt_shode+timedelta(days=30)
        now = datetime.datetime.now()
        days_left = finish_time - now  # seconds
        rooz = days_left/86400
        return rooz

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
    brand_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    learn = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'upc', 'title', 'brand', 'brand_name', 'category', 'category_name', 'weight', 'price', 'name_type', 'product_type',
                  'is_active', 'user', 'description', 'create_time', 'days_left', 'images', 'attr_value', 'learn')

    def get_user(self, obj):
        name2 = obj.user.info.name + " " + obj.user.info.family
        return name2

    def get_learn(self, obj):
        result = []
        type = obj.product_type
        print(type.id)
        learns = Learn.objects.filter(type=type)
        print(learns)
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

    def get_brand_name(self, obj):
        brand_name = obj.brand.name
        return brand_name

    def get_category_name(self, obj):
        category_name = obj.category.name
        return category_name

    def get_days_left(self, obj):
        sabt_shode = obj.create_time
        finish_time = sabt_shode+timedelta(days=30)
        now = datetime.datetime.now()
        days_left = finish_time - now  # seconds
        rooz = days_left/86400
        return rooz

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