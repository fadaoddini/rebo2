from django.contrib import admin
from django.contrib.admin import register
from django.forms import BaseInlineFormSet

from catalogue.models import Category, Brand, Product, ProductType, ProductAttribute, ProductAttributeValue, \
    ProductImage, ProductAttr


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


class ProductAttrInline(admin.TabularInline):
    model = ProductAttr
    extra = 2


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('price', 'weight', 'sell_buy', 'product_type', 'user',
                    'is_active', 'is_successful')
    list_filter = ('is_active', 'sell_buy')
    list_editable = ('is_active',)
    search_fields = ('upc', 'user')
    actions = ('active_all', 'deactive_all')
    inlines = [ProductImageInline, ProductAttrInline]

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


class ProductAttrAdmin(admin.ModelAdmin):
    list_display = ('title', 'value')


@register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_type')
    search_fields = ('title', 'product_type')
    inlines = [ProductAttributeValueInline]


@register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)
    inlines = [ProductAttributeInline]


@register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('value', 'product_attribute')

    def get_list_display(self, request):
        print(request.user.info.is_active)
        return self.list_display


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


@register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)



