# Generated by Django 3.2 on 2024-02-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/feae2e00-d2bd-44ef-a100-9e765afa0664/'),
        ),
    ]
