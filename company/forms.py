from django import forms
from django.core.exceptions import ValidationError

from company.models import Company, Location, Staff


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'image']
        # exclude = ['user', 'is_active']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'family', 'mobile', 'age', 'jens', 'is_married', 'card_number', 'role', 'codemeli',
                  'insurance', 'insurance_status', 'fix_salary', 'salon', 'status']


