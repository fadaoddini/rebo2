# Generated by Django 3.2 on 2024-02-28 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/115a3447-dcbb-472e-9df2-d3b03399100e/'),
        ),
    ]
