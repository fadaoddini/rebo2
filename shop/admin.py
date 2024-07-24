from django.contrib import admin
from django.contrib.admin import register

from shop.models import Product, ProductImage, Category, Brand, Package, Location


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('price', 'warranty', 'weight', 'category', 'brand', 'user', 'number_exist',
                    'upc', 'is_active')
    list_filter = ('is_active', 'number_exist', 'warranty', 'category', 'brand')
    list_editable = ('is_active',)
    search_fields = ('upc', 'user')
    actions = ('active_all', 'deactive_all')
    inlines = [ProductImageInline,]

    def active_all(self, request, queryset):
        for queryone in queryset:
            product = Product.objects.filter(pk=queryone.pk).first()
            product.is_active = True
            product.save()

    def deactive_all(self, request, queryset):
            for queryone in queryset:
                product = Product.objects.filter(pk=queryone.pk).first()
                product.is_active = False
                product.save()


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('images',)


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


@register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


@register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'ostan', 'shahr', 'codeposti')
    search_fields = ('codeposti', 'ostan', 'shahr')




