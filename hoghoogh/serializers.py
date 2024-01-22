from rest_framework import serializers

from hoghoogh.models import Amar


class AmarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amar
        fields = ('id', 'staff', 'listprice', 'name', 'price', 'tedad', 'type', 'is_sarparast', 'tarikh')

    def create(self, validated_data):
        key = validated_data.pop('key')
        instance = super().create(validated_data)
        return instance


