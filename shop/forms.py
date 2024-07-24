from django import forms

from shop.models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'family', 'mobile', 'address', 'ostan', 'shahr', 'codeposti']


class CartAddLocationForm(forms.Form):
    location_count = forms.IntegerField(max_value=10)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)