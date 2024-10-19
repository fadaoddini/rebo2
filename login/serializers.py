from rest_framework import serializers

from login.models import MyUser, Follow, Address


class MyUserSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'status', 'image', 'mobile', 'id')

    def get_status(self, obj):
        status = "Nothing"
        first_name = obj.first_name
        last_name = obj.last_name
        if (first_name != "") and (last_name != ""):
            status = "Ok"

        return status



class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'followed', 'created_at']



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','receiver_name', 'address', 'postal_code', 'phone', 'city', 'sub_city', 'is_active']
