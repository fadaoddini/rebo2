# Generated by Django 5.1 on 2024-08-28 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0032_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/ba00ef2e-5ae9-4b56-9e34-170001b8cdbc/'),
        ),
    ]
