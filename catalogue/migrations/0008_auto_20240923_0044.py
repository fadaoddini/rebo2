# Generated by Django 3.2 on 2024-09-23 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_auto_20240922_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d/types/'),
        ),
        migrations.AddField(
            model_name='producttype',
            name='name',
            field=models.CharField(blank=True, max_length=42, null=True),
        ),
    ]