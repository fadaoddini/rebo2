# Generated by Django 3.2 on 2024-09-23 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20240923_0044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='title',
        ),
    ]
