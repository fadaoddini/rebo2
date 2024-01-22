from django.urls import path, re_path

from law.views import Law


urlpatterns = [
    path('', Law.as_view(), name='law'),
]
