# Generated by Django 4.2 on 2024-01-15 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/1df6a76a-57de-4e5f-854a-6a3eec1af39b/'),
        ),
    ]