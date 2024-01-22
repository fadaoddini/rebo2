from django.contrib import admin
from django.contrib.admin import register
from learn.models import Learn, Section, Lesson, Category


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)


@register(Learn)
class LearnAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'type', 'is_free', 'auther', 'user', 'is_active')
    list_filter = ('is_active', 'type', 'is_free')
    list_editable = ('is_active', 'is_free')
    search_fields = ('title', 'auther')
    actions = ('active_all', 'deactive_all', 'free_all', 'cash_all')

    def active_all(self, request, queryset):
        for queryone in queryset:
            learn = Learn.objects.filter(pk=queryone.pk).first()
            learn.is_active = True
            learn.save()

    def deactive_all(self, request, queryset):
        for queryone in queryset:
            learn = Learn.objects.filter(pk=queryone.pk).first()
            learn.is_active = False
            learn.save()

    def free_all(self, request, queryset):
        for queryone in queryset:
            learn = Learn.objects.filter(pk=queryone.pk).first()
            learn.is_free = True
            learn.save()

    def cash_all(self, request, queryset):
        for queryone in queryset:
            learn = Learn.objects.filter(pk=queryone.pk).first()
            learn.is_free = False
            learn.save()


@register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'learn', 'is_free', 'is_active')
    list_filter = ('is_active', 'learn_id__title', 'is_free')
    list_editable = ('is_active', 'is_free')
    search_fields = ('title', 'learn_id__title')
    actions = ('active_all', 'deactive_all', 'free_all', 'cash_all')

    def active_all(self, request, queryset):
        for queryone in queryset:
            section = Section.objects.filter(pk=queryone.pk).first()
            section.is_active = True
            section.save()

    def deactive_all(self, request, queryset):
        for queryone in queryset:
            section = Section.objects.filter(pk=queryone.pk).first()
            section.is_active = False
            section.save()

    def free_all(self, request, queryset):
        for queryone in queryset:
            section = Section.objects.filter(pk=queryone.pk).first()
            section.is_free = True
            section.save()

    def cash_all(self, request, queryset):
        for queryone in queryset:
            section = Section.objects.filter(pk=queryone.pk).first()
            section.is_free = False
            section.save()


@register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'is_free', 'is_active')
    list_filter = ('is_active', 'section_id__title', 'is_free')
    list_editable = ('is_active', 'is_free')
    search_fields = ('title', 'section_id__title')
    actions = ('active_all', 'deactive_all', 'free_all', 'cash_all')

    def active_all(self, request, queryset):
        for queryone in queryset:
            lesson = Lesson.objects.filter(pk=queryone.pk).first()
            lesson.is_active = True
            lesson.save()

    def deactive_all(self, request, queryset):
        for queryone in queryset:
            lesson = Lesson.objects.filter(pk=queryone.pk).first()
            lesson.is_active = False
            lesson.save()

    def free_all(self, request, queryset):
        for queryone in queryset:
            lesson = Lesson.objects.filter(pk=queryone.pk).first()
            lesson.is_free = True
            lesson.save()

    def cash_all(self, request, queryset):
        for queryone in queryset:
            lesson = Lesson.objects.filter(pk=queryone.pk).first()
            lesson.is_free = False
            lesson.save()



