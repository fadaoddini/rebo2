# Generated by Django 5.1 on 2024-08-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0033_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/6c015e4a-5d01-43bd-b05f-b3e1f19eadba/'),
        ),
    ]
