# Generated by Django 3.2 on 2024-08-17 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0029_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/d2a3e786-2d4b-4252-8d2d-277e57ced5df/'),
        ),
    ]