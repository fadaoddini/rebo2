# Generated by Django 3.2 on 2024-08-12 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/00b06f46-6365-477a-b52e-c2b3c589f527/'),
        ),
    ]