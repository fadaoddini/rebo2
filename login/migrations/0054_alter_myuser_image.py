# Generated by Django 5.1 on 2024-09-09 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0053_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/a5949601-2982-4de3-a325-26be98669aea/'),
        ),
    ]