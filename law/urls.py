from django.urls import path, re_path

from law.views import Law, LawListView, FAQListView


urlpatterns = [
    path('all_laws/', LawListView.as_view(), name='all-law-api'),  # نمایش تمام قوانین
    path('all_faqs/', FAQListView.as_view(), name='all-faq-api'),  # نمایش تمام سوالات متداول
]
