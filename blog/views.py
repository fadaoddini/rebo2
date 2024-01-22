from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from blog.models import Blog, Category


def blog_list(request, year=None, month=None):
    if month is not None:
        return HttpResponse(f"blog list {year} - {month}")
    if year is not None:
        return HttpResponse(f"blog list {year}")

    return HttpResponse(f"blog list")


def category_blog_list(request):
    return HttpResponse("category_blog_list")


def detail_blog(request, title):
    return HttpResponse(f"detail_blog {title}")


class SingleBlogWeb(View):
    template_name = 'web/blog/single.html'

    def get(self, request, pk, *args, **kwargs):
        context = dict()
        blog = Blog.objects.filter(pk=pk).first()
        context['blog'] = blog
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class BlogWeb(View):
    template_name = 'web/blog/index.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        categories = Category.objects.prefetch_related('blogs').all()
        blogs = Blog.objects.select_related('category').filter(status=True).all()
        print(categories[0].blogs.all())
        context['blogs'] = blogs
        context['categories'] = categories
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class BlogWebPk(View):
    template_name = 'web/blog/blog.html'

    def get(self, request, pk, *args, **kwargs):
        context = dict()
        category = Category.objects.filter(pk=pk).first()
        blogs = Blog.objects.filter(category=pk).all()
        context['blogs'] = blogs
        context['category'] = category
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)
