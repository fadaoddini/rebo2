from django import forms
from django.forms import ModelForm, inlineformset_factory

from catalogue.models import Product, ProductImage, ProductAttributeValue, ProductType, ProductAttribute, ProductAttr


class AjaxProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['title', ]


class SellProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['price', 'weight', 'description', 'warranty']
        # exclude = ['user', 'is_active']


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        exclude = ()


class ProductAttrForm(ModelForm):
    class Meta:
        model = ProductAttr
        exclude = ()


class ProductAttributeForm(ModelForm):

    class Meta:
        model = ProductAttributeValue
        fields = ['product_attribute', 'value']

    def clean_product_attribute(self):
        product_attribute = self.cleaned_data['product_attribute']
        print("clean_product_attribute")
        print(product_attribute)
        print("clean_product_attribute")
        return product_attribute

    def clean(self):
        cleaned_data = super().clean()
        print("cleaned_data")
        print(cleaned_data)
        print("cleaned_data")
        return cleaned_data


ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=2)
ProductAttrFormSet = inlineformset_factory(Product, ProductAttr, form=ProductAttrForm, extra=2)


class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        product_type = kwargs.pop('product_type')
        print("((((((((((((((((((((((((((((((((((((((((((((((")
        print(product_type.first().pk)
        print("((((((((((((((((((((((((((((((((((((((((((((((")
        super().__init__(*args, **kwargs)
        self.fields['product_type'].queryset = product_type
    product_type = forms.ModelChoiceField(queryset=ProductAttribute.objects.filter(product_type=1))