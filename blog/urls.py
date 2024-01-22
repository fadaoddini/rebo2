from django.urls import path, re_path

from blog.views import blog_list, category_blog_list, detail_blog, SingleBlogWeb, BlogWeb, BlogWebPk

urlpatterns = [
    path('list/', blog_list),
    path('detail/<str:title>', detail_blog),
    path('categories/list/', category_blog_list),
    path('archive/<int:year>/', blog_list),
    re_path(r'archive/?P<year>[0-9]{4}/', blog_list),
    path('single/<int:pk>/', SingleBlogWeb.as_view(), name='blog-single-web'),
    path('blog/', BlogWeb.as_view(), name='blog-web'),
    path('blog/<int:pk>/', BlogWebPk.as_view(), name='blog-web-pk'),
    path('archive/<int:year>/<int:month>/', blog_list)
]
