# Generated by Django 3.2 on 2024-08-14 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/6bee086f-3a04-4502-9955-9a5022b23da5/'),
        ),
    ]