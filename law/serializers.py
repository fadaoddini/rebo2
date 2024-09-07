# law/serializers.py

from rest_framework import serializers
from .models import Law, FAQ


class LawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Law
        fields = ['id', 'title', 'text', 'role', 'is_active', 'create_time', 'modified_time']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'is_active', 'create_time', 'modified_time']
