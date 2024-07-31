from rest_framework import serializers
from catalogue.models import Product, ProductImage, ProductAttribute, ProductAttributeValue, Brand, Category, \
    ProductType
import datetime
from datetime import timedelta
from django.db.models import Max

from learn.models import Learn


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ('id', 'title')


class ProductSellSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    name_type = serializers.SerializerMethodField()
    attr_value = serializers.SerializerMethodField()
    finished_time = serializers.SerializerMethodField()
    top_price_bid = serializers.SerializerMethodField()
    count_bid = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'upc', 'weight', 'price', 'name_type', 'product_type', 'sell_buy', 'top_price_bid', 'count_bid',
                  'is_active', 'user', 'description', 'create_time', 'finished_time', 'images', 'attr_value')

    def get_user(self, obj):
        name2 = obj.user.first_name + " " + obj.user.last_name
        return name2

    def get_name_type(self, obj):
        id_type = obj.product_type
        return id_type.title

    def get_count_bid(self, obj):
        return obj.bids.count()

    def get_top_price_bid(self, obj):

        top_price_bid = obj.bids.aggregate(Max('price'))['price__max']
        return top_price_bid if top_price_bid is not None else 0

    def get_finished_time(self, obj):
        sabt_shode = obj.create_time

        finish_time = sabt_shode+timedelta(days=30)
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