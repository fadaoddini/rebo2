# Generated by Django 5.1 on 2024-09-03 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0042_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/50ddf55e-a58a-449a-b170-e2bd0f094ea8/'),
        ),
    ]