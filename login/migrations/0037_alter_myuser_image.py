# Generated by Django 5.1 on 2024-09-02 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0036_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/2f60d42b-eba3-4bbe-91bd-224984d3b5df/'),
        ),
    ]
