from django.contrib import admin
from .models import Category, Attribute, Divar, DivarAttribute, DivarImage, AttributeValue


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1
    fields = ('value',)  # فقط فیلد value را نمایش می‌دهد


class DivarAttributeInline(admin.TabularInline):
    model = DivarAttribute
    extra = 1
    fields = ('attribute', 'value')  # فیلدهای مورد نیاز برای اضافه کردن ویژگی‌ها و مقادیر آن‌ها


class DivarImageInline(admin.TabularInline):
    model = DivarImage
    extra = 1
    fields = ('image',)  # فقط فیلد image را نمایش می‌دهد


class DivarAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_time', 'status', 'ispay', 'user')
    list_filter = ('category', 'status', 'ispay')
    search_fields = ('title', 'description')
    inlines = [DivarImageInline, DivarAttributeInline]
    # تنظیمات اضافی مانند list_editable و list_per_page نیز می‌توانند به اینجا اضافه شوند


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    inlines = [AttributeValueInline]
    # تنظیمات اضافی مانند search_fields و list_editable نیز می‌توانند به اینجا اضافه شوند


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Divar, DivarAdmin)
admin.site.register(DivarAttribute)  # ثبت DivarAttribute بدون inline چون inline فقط در DivarAdmin است
admin.site.register(DivarImage)  # ثبت DivarImage بدون inline چون inline فقط در DivarAdmin است
admin.site.register(AttributeValue)  # ثبت AttributeValue بدون inline چون inline فقط در AttributeAdmin است
