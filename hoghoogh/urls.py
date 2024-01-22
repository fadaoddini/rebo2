from django.urls import path, re_path

from hoghoogh.views import hoghoogh_list, setting_hoghoogh, update_setting_hoghoogh, \
    update_setting_hoghoogh_send, update_setting_hoghoogh_edit, listprice, add_listprice, add_amar, amar, edit_amar, \
    delete_item_amar, checklist_staff_amar, add_hoghogh_first, delete_all_item_amar_by_staff, taeed_all_hoghoogh, \
    archive_hoghoogh_delete_before

urlpatterns = [
    path('list/', hoghoogh_list, name='hoghoogh_list'),
    path('setting_h/', setting_hoghoogh, name='setting-hoghoogh'),
    path('setting_h_u/<int:pk>/', update_setting_hoghoogh, name='update-setting-hoghoogh'),
    path('setting_h_u_s/<int:pk>/', update_setting_hoghoogh_send, name='update-setting-hoghoogh-send'),
    path('setting_h_u_e/<int:pk>/', update_setting_hoghoogh_edit, name='update-setting-hoghoogh-edit'),
    path('listprice/<int:pk>/', listprice, name='listprice'),
    path('add_listprice/<int:pk>/', add_listprice, name='add-listprice'),
    path('amar/<int:pk>/', amar, name='amar'),
    path('add_amar/<int:pk>/', add_amar, name='add-amar'),
    path('add_hoghogh_first/<int:pk>/', add_hoghogh_first, name='add-hoghogh-first'),
    path('edit_amar/<int:pk>/', edit_amar, name='edit-amar'),
    path('delete_item_amar/<int:pk>/', delete_item_amar, name='delete-edit-amar'),
    path('delete_all_item_amar_by_staff/<int:pk>/', delete_all_item_amar_by_staff, name='delete-all-amar_staff'),
    path('checklist_staff_amar/<int:pk>/', checklist_staff_amar, name='checklist-staff-amar'),
    path('archive_all_hoghoogh/<int:pk>/', archive_hoghoogh_delete_before, name='archive-location-hoghoogh'),
    path('taeed/<int:pk>/', taeed_all_hoghoogh, name='taeed-all-hoghoogh'),
]
