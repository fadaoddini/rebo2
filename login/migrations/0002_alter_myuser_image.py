# Generated by Django 4.2 on 2024-01-12 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/359e8498-fd97-4306-b7b9-77f8f55d2096/'),
        ),
    ]
