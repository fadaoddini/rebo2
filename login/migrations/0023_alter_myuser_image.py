# Generated by Django 3.2 on 2024-08-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0022_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/bd2aa807-f9e2-45ac-8cad-9f60f40681f4/'),
        ),
    ]
