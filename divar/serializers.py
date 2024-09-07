from rest_framework import serializers
from divar.models import Divar, DivarAttribute, DivarImage, AttributeValue, Category, Attribute


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'image']


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value']


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'values']


class DivarAttributeSerializer(serializers.ModelSerializer):
    attribute = serializers.StringRelatedField()
    value = AttributeValueSerializer()

    class Meta:
        model = DivarAttribute
        fields = ['attribute', 'value']


class DivarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivarImage
        fields = ['image']


class DivarSerializer(serializers.ModelSerializer):
    images = DivarImageSerializer(many=True, read_only=True)
    divar_attributes = DivarAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Divar
        fields = [
            'id', 'category', 'title', 'description', 'nardeban', 'fori',
            'status', 'created_time', 'modified_time', 'expired_time',
            'ispay', 'user', 'images', 'divar_attributes'
        ]