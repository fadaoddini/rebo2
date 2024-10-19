from rest_framework import serializers

from .models import Bid


class BidSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    sellbuy = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ['product', 'price', 'user', 'result', 'mobile', 'sellbuy', 'total', 'image_url', 'weight']

    def get_image_url(self, obj):
        request = self.context.get('request')  # گرفتن request از context
        if obj.user.image and request:
            return request.build_absolute_uri(obj.user.image.url)  # ایجاد URL کامل
        return None

    def get_user(self, obj):
        if (obj.user.first_name == "" and obj.user.last_name == ""):
            return "ناشناس"
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_mobile(self, obj):
        return obj.user.mobile

    def get_sellbuy(self, obj):
        return obj.product.sell_buy

    def get_total(self, obj):
        return obj.weight * obj.price


