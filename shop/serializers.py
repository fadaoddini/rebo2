import datetime
from datetime import timedelta
from rest_framework import serializers

from shop.models import Product, MyShop, ProductImage


class ProductShopSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    my_shop = serializers.SerializerMethodField()
    id_shop = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    package = serializers.SerializerMethodField()
    finished_time = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'upc', 'weight', 'price', 'my_shop', 'category', 'package', 'discount', 'vije', 'number_exist',
                  'is_active', 'user', 'description', 'create_time', 'finished_time', 'images', 'discount_price',
                  'number_send', 'id_shop', 'title')

    def get_user(self, obj):
        name2 = obj.user.first_name + " " + obj.user.last_name
        return name2

    def get_my_shop(self, obj):
        name = obj.my_shop.name_shop
        return name

    def get_id_shop(self, obj):
        id = obj.my_shop.id
        return id

    def get_category(self, obj):
        name = obj.category.name
        return name

    def get_package(self, obj):
        name = obj.package.title
        return name

    def get_finished_time(self, obj):
        sabt_shode = obj.create_time
        finish_time = sabt_shode+timedelta(days=30)
        return finish_time

    def get_discount_price(self, obj):
        price = obj.price
        discount = obj.discount
        price_discount = (price * discount)/100
        all_price_discount = price - price_discount
        return int(all_price_discount)

    def get_images(self, obj):
        return ImageSerializer(obj.images_shop.all(), many=True).data


class MyShopSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    finished_time = serializers.SerializerMethodField()

    class Meta:
        model = MyShop
        fields = ('id', 'name_shop', 'administrator', 'mobile', 'code_posti', 'address',
                  'is_active', 'user', 'image', 'created_time', 'finished_time')

    def get_user(self, obj):
        name2 = obj.user.first_name + " " + obj.user.last_name
        return name2

    def get_finished_time(self, obj):
        sabt_shode = obj.created_time
        finish_time = sabt_shode+timedelta(days=30)
        return finish_time


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', )