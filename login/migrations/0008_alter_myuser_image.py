# Generated by Django 3.2 on 2024-02-26 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/92ae136f-b042-4f1e-810e-1488810474a9/'),
        ),
    ]
