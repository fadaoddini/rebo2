# Generated by Django 5.1 on 2024-09-02 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0038_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/87e29a86-e10d-4e20-afce-b80de65b7692/'),
        ),
    ]
