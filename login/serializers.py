from rest_framework import serializers

from login.models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'status')

    def get_status(self, obj):
        status = "Nothing"
        first_name = obj.first_name
        last_name = obj.last_name
        if (first_name != "") and (last_name != ""):
            status = "Ok"

        return status


