from django import forms
from learn.models import Learn, Section, Lesson


class LearnForm(forms.ModelForm):
    class Meta:
        model = Learn
        fields = ['auther', 'type', 'title', 'price', 'image', 'category']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title', 'learn']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['video', 'section', 'title', 'image', 'description']


