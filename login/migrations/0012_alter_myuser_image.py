# Generated by Django 3.2 on 2024-08-12 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/b16dd022-9871-46c7-a43f-eef91961cd8d/'),
        ),
    ]
