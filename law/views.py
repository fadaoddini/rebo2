from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import generics
from law.models import Law, FAQ
from law.serializers import LawSerializer, FAQSerializer


# law/views.py
class LawListView(generics.ListAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer


class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
