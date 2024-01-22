from django.db import models
from django.contrib.auth import get_user_model as user_model

from catalogue.models import ProductType


class Category(models.Model):
    title = models.CharField(max_length=48)
    image = models.ImageField(upload_to='%Y/%m/%d/img-category-learn/', null=True, blank=True)
    created_time = models.DateTimeField(auto_now=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.title}"


class Learn(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_LEARN = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )

    FREE = True
    CASH = False

    STATUS_TYPE = (
        (FREE, 'رایگان'),
        (CASH, 'نقدی'),
    )

    User = user_model()
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    auther = models.CharField(max_length=48)
    type = models.ForeignKey(ProductType, on_delete=models.RESTRICT, null=True, related_name="learns")
    title = models.CharField(max_length=48)
    price = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to='%Y/%m/%d/learns/')
    is_active = models.BooleanField(choices=STATUS_LEARN, default=INACTIVE)
    is_free = models.BooleanField(choices=STATUS_TYPE, default=CASH)
    created_time = models.DateTimeField(auto_now=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='learns')

    class Meta:
        verbose_name = 'Learn'
        verbose_name_plural = 'Learns'

    def __str__(self):
        return f"{self.title}"


class Section(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_LEARN = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )

    FREE = True
    CASH = False

    STATUS_TYPE = (
        (FREE, 'رایگان'),
        (CASH, 'نقدی'),
    )

    title = models.CharField(max_length=48)
    learn = models.ForeignKey(Learn, on_delete=models.RESTRICT, related_name="sections")
    is_active = models.BooleanField(choices=STATUS_LEARN, default=INACTIVE)
    is_free = models.BooleanField(choices=STATUS_TYPE, default=CASH)
    created_time = models.DateTimeField(auto_now=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return f"{self.title}"


class Lesson(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_LEARN = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )

    FREE = True
    CASH = False

    STATUS_TYPE = (
        (FREE, 'رایگان'),
        (CASH, 'نقدی'),
    )

    title = models.CharField(max_length=48)
    section = models.ForeignKey(Section, on_delete=models.RESTRICT, related_name="lessons")
    image = models.ImageField(upload_to='%Y/%m/%d/img-lessons/', null=True, blank=True)
    video = models.FileField(upload_to='%Y/%m/%d/video-lessons/', null=True, blank=True)
    three1 = models.FileField(upload_to='%Y/%m/%d/three1/', null=True, blank=True)
    three2 = models.FileField(upload_to='%Y/%m/%d/three2/', null=True, blank=True)
    voice = models.FileField(upload_to='%Y/%m/%d/voice/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(choices=STATUS_LEARN, default=INACTIVE)
    is_free = models.BooleanField(choices=STATUS_TYPE, default=CASH)
    created_time = models.DateTimeField(auto_now=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f"{self.title}"

