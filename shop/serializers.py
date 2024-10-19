import datetime
import random
from datetime import timedelta
from rest_framework import serializers

from shop.models import Product, MyShop, ProductImage, Category, Package, BasketLine, Basket


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'title', 'create_time', 'modified_time')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductShopSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    my_shop = serializers.SerializerMethodField()
    id_shop = serializers.SerializerMethodField()
    category = CategorySerializer()  # استفاده از CategorySerializer
    sub_category = CategorySerializer()  # استفاده از CategorySerializer
    package = PackageSerializer()  # استفاده از PackageSerializer
    finished_time = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'upc', 'weight', 'price', 'my_shop', 'category', 'sub_category', 'package', 'discount', 'vije',
                  'number_exist', 'is_active', 'user', 'description', 'create_time', 'finished_time',
                  'images', 'discount_price', 'number_send', 'id_shop', 'title')

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()

    def get_my_shop(self, obj):
        return obj.my_shop.name_shop

    def get_id_shop(self, obj):
        return obj.my_shop.id

    def get_category(self, obj):
        return CategorySerializer(obj.category).data

    def get_sub_category(self, obj):
        return CategorySerializer(obj.sub_category).data

    def get_package(self, obj):
        return PackageSerializer(obj.package).data

    def get_finished_time(self, obj):
        finish_time = obj.create_time + timedelta(days=30)
        return finish_time

    def get_discount_price(self, obj):
        try:
            price = float(obj.price)  # تبدیل به float
            discount = float(obj.discount)  # تبدیل به float
        except ValueError:
            return 0  # یا مقدار پیش‌فرض دیگری

        price_discount = (price * discount) / 100
        return int(price - price_discount)

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
        return f"{obj.user.first_name} {obj.user.last_name}".strip()

    def get_finished_time(self, obj):
        return obj.created_time + timedelta(days=30)


class BasketLineSerializer(serializers.ModelSerializer):
    product = ProductShopSerializer()  # استفاده از ProductShopSerializer برای نمایش جزئیات محصول

    class Meta:
        model = BasketLine
        fields = ('product', 'count', 'price', 'discount', 'total_price')

class BasketSerializer(serializers.ModelSerializer):
    basket_lines = BasketLineSerializer(many=True, source='baskets_line')

    class Meta:
        model = Basket
        fields = ('id', 'user', 'basket_date', 'basket_lines')