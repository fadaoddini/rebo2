# Generated by Django 5.1 on 2024-09-03 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0044_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/f4f6d072-c068-4b34-a713-7c1615dd350c/'),
        ),
    ]
