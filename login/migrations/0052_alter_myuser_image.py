# Generated by Django 5.1 on 2024-09-07 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0051_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/22e9fcfa-97c8-4cba-badb-dfc56965bcc7/'),
        ),
    ]