from django.urls import path, re_path

from company.views import customer_list, get_report, get_report_by_customer, add_balance_customer, \
    add_balance_all_customer, transfer_transaction, create_company, location_list, add_location, add_staff, \
    create_staff, staff_list, edit_staff, update_staff, delete_staff, archive_all_hoghoogh, archive_all_hoghoogh_all

urlpatterns = [
    path('list/', customer_list, name='customer_list'),
    path('locations/', location_list, name='location-list'),
    path('add_location/', add_location, name='add-location'),
    path('staff/<int:pk>/', staff_list, name='staff-list'),
    path('archive_all_hoghoogh/<int:pk>/', archive_all_hoghoogh, name='archive-all-hoghoogh'),
    path('archive_all_hoghoogh_all/<int:pk>/', archive_all_hoghoogh_all, name='archive-all-hoghoogh-all'),
    path('create_staff/<int:pk>/', create_staff, name='create-staff'),
    path('edit_staff/<int:pk>/', edit_staff, name='edit-staff'),
    path('add_staff/<int:pk>/', add_staff, name='add-staff'),
    path('update_staff/<int:pk>/', update_staff, name='update-staff'),
    path('delete_staff/<int:pk>/', delete_staff, name='delete-staff'),
    path('add_company/', create_company, name='create-company'),
    path('report/all/', get_report, name='report_all_customer'),
    path('report/customer/<int:pk>/', get_report_by_customer, name='get_report_by_customer'),
    path('balance/customer/<int:pk>/<int:typedate>/', add_balance_customer, name='add_balance_customer'),
    path('balance/all/', add_balance_all_customer, name='add_balance_all_customer'),
    path('transfer/<int:sender>/<int:receiver>/<int:typedate>/<int:quantity>/<int:driver>/',
         transfer_transaction, name='add_balance_all_customer'),
]
