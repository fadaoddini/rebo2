# Generated by Django 3.2 on 2024-02-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/ea72562d-ac60-4aca-8efe-7b662ea7b23a/'),
        ),
    ]
