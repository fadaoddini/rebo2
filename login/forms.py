from django import forms

from login import models


class RegisterUser(forms.ModelForm):
    class Meta:
        model = models.MyUser
        fields = ['mobile', ]


class NameUserForm(forms.ModelForm):
    class Meta:
        model = models.MyUser
        fields = ['first_name', 'last_name', 'password' ]
