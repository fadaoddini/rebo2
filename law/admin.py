from django.contrib import admin
from .models import Law, FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.admin import register


@register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active')
    list_editable = ('is_active',)


class LawAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())  # استفاده از CKEditor

    class Meta:
        model = Law
        fields = '__all__'


class LawAdmin(admin.ModelAdmin):
    form = LawAdminForm


admin.site.register(Law, LawAdmin)