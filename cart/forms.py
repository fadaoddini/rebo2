from django import forms

PRODUCT_COUNT_CHOICES = [(i, str(i)) for i in range(1, 3)]


class CartAddProductForm(forms.Form):
    product_count = forms.TypedChoiceField(choices=PRODUCT_COUNT_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartAddLocationForm(forms.Form):
    location_count = forms.IntegerField(required=False, max_value=10, widget=forms.HiddenInput)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)