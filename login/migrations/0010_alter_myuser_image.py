# Generated by Django 4.2 on 2024-01-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/f4141a30-35b6-4a00-8edb-fc9844a5da79/'),
        ),
    ]
