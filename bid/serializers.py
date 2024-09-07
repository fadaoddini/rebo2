from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bid, Product


class BidSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    sellbuy = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ['product', 'price', 'user', 'result', 'mobile', 'sellbuy']

    def get_user(self, obj):
        name2 = obj.user.first_name + " " + obj.user.last_name
        return name2

    def get_mobile(self, obj):
        mobile = obj.user.mobile
        return mobile

    def get_sellbuy(self, obj):
        sell_buy = obj.product.sell_buy
        return sell_buy

