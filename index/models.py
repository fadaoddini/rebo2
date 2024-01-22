from django.db import models


class SettingApp(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_OPEN = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    favicon = models.ImageField(upload_to='settings/', null=True, blank=True)
    logo = models.ImageField(upload_to='settings/', null=True, blank=True)
    login_text = models.TextField(blank=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    about_text = models.TextField(blank=True)
    footer_text = models.TextField(blank=True)
    is_active = models.BooleanField(choices=STATUS_OPEN, default=ACTIVE)

    class Meta:
        verbose_name = 'setting'
        verbose_name_plural = 'settings'

    def __str__(self):
        return self.title


