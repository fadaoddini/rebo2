from django.db import models
from ckeditor.fields import RichTextField


class Law(models.Model):
    # تعریف رول‌ها
    MARKET = 1
    TRANSPORT = 2
    SHOP = 3
    EDUCATION = 4
    REGISTRATION = 5

    ROLE_CHOICES = (
        (MARKET, 'بازار'),
        (TRANSPORT, 'حمل و نقل'),
        (SHOP, 'فروشگاه'),
        (EDUCATION, 'آموزش'),
        (REGISTRATION, 'ثبت نام'),
    )

    title = models.CharField(max_length=255)  # عنوان قانون
    text = RichTextField()  # استفاده از CKEditor برای فیلد متن
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)  # نقش مربوطه

    is_active = models.BooleanField(default=True)  # فعال یا غیرفعال بودن قانون
    create_time = models.DateTimeField(auto_now_add=True)  # زمان ایجاد
    modified_time = models.DateTimeField(auto_now=True)  # زمان ویرایش

    class Meta:
        verbose_name = 'Law'
        verbose_name_plural = 'Laws'

    def __str__(self):
        return f"{self.title} - {self.get_role_display()}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    is_active = models.BooleanField(default=True)  # فعال/غیرفعال بودن سوال
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question
