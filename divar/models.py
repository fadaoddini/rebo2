from django.db import models
from login.models import MyUser


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    image = models.ImageField(upload_to='divar/category/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'
        ordering = ['name']

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Attribute Value'
        verbose_name_plural = 'Attribute Values'
        ordering = ['value']
        unique_together = ('attribute', 'value')

    def __str__(self):
        return self.value


class Divar(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='divars')
    title = models.CharField(max_length=255)
    description = models.TextField()
    nardeban = models.BooleanField(default=False)
    fori = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    expired_time = models.DateTimeField(null=True, blank=True)
    ispay = models.BooleanField(default=False)
    user = models.ForeignKey(MyUser, related_name='divars', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Divar'
        verbose_name_plural = 'Divars'
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.title} by {self.user}"


class DivarAttribute(models.Model):
    divar = models.ForeignKey(Divar, on_delete=models.CASCADE, related_name='divar_attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Divar Attribute'
        verbose_name_plural = 'Divar Attributes'
        unique_together = ('divar', 'attribute')  # Ensure a divar can only have one value per attribute

    def __str__(self):
        return f"{self.divar.title} - {self.attribute.name}: {self.value.value}"


class DivarImage(models.Model):
    image = models.ImageField(upload_to='divar/images/%Y/%m/%d/', null=True, blank=True)
    product = models.ForeignKey(Divar, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Divar Image'
        verbose_name_plural = 'Divar Images'

    def __str__(self):
        return str(self.product)
