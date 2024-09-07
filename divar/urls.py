from django.urls import path
from divar.views import DivarListCreateView, DivarDetailView, CategoryListView, AttributeListView, DivarImageUploadView

urlpatterns = [
    path('divars/', DivarListCreateView.as_view(), name='divar-list-create'),  # برای لیست کردن و ایجاد آگهی‌ها
    path('divars/<int:pk>/', DivarDetailView.as_view(), name='divar-detail'),  # برای مشاهده، ویرایش و حذف یک آگهی خاص
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/attributes/', AttributeListView.as_view(), name='attribute-list'),
    path('divars/<int:divar_id>/upload-image/', DivarImageUploadView.as_view(), name='divar-image-upload'),
]
